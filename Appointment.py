import gradio as gr
import requests
import json
from datetime import datetime

URL = "https://api.scaledown.xyz/compress/raw/"

HEADERS = {
    "x-api-key": 'API KEY',
    "Content-Type": "application/json"
}

INTERNAL_CONTEXT = (
    "You are an appointment reminder assistant. "
    "Only generate short reminder messages for appointments."
)

appointments = []


def make_key(appt):
    return f"{appt['title']}|{appt['date']}|{appt['time']}|{appt['location']}"

def appointment_exists(new_appt):
    for a in appointments:
        if make_key(a) == make_key(new_appt):
            return True
    return False

def format_all_appointments():
    if not appointments:
        return "No appointments stored."

    lines = []
    for i, a in enumerate(appointments, 1):
        lines.append(
            f"{i}. {a['title']} | {a['date']} {a['time']} | {a['location']} | {a['notes']}"
        )
    return "\n".join(lines)

# ================= AUTO DELETE PAST =================

def remove_past_appointments():
    now = datetime.now()
    appointments[:] = [
        appt for appt in appointments
        if safe_future(appt)
    ]

def safe_future(appt):
    try:
        appt_dt = datetime.strptime(
            f"{appt['date']} {appt['time']}",
            "%Y-%m-%d %H:%M"
        )
        return appt_dt >= datetime.now()
    except:
        return False

# ================= API =================

def compress_context(context, appointment):
    try:
        payload = {
            "context": context,
            "appointment": appointment,
            "prompt": "Generate reminder",
            "scaledown": {"rate": "auto"}
        }

        r = requests.post(URL, headers=HEADERS, json=payload, timeout=15)
        data = r.json()

        if not data.get("successful"):
            return None, data.get("error", "Compression failed")

        return data["results"]["compressed_prompt"], None

    except Exception as e:
        return None, str(e)

# ================= CORE =================

def generate_reminder_message(appointment):
    return (
        f"Reminder: {appointment['title']} on "
        f"{appointment['date']} at {appointment['time']} "
        f"at {appointment['location']}. "
        f"Notes: {appointment['notes']}"
    )

def add_appointment(title, date, time, location, notes):
    remove_past_appointments()

    appointment = {
        "title": title.strip(),
        "date": date.strip(),
        "time": time.strip(),
        "location": location.strip(),
        "notes": notes.strip()
    }

    if not title or not date or not time:
        return "Missing required fields.", format_all_appointments()

    if appointment_exists(appointment):
        return "Duplicate appointment not added.", format_all_appointments()

    compressed, err = compress_context(INTERNAL_CONTEXT, appointment)

    if err:
        return f"Error: {err}", format_all_appointments()

    appointment["compressed"] = compressed
    appointments.append(appointment)

    return "Appointment stored successfully.", format_all_appointments()

def check_one_hour_reminders():
    remove_past_appointments()

    now = datetime.now()
    reminders = []

    for appt in appointments:
        try:
            appt_dt = datetime.strptime(
                f"{appt['date']} {appt['time']}",
                "%Y-%m-%d %H:%M"
            )

            diff_minutes = (appt_dt - now).total_seconds() / 60

            # show all reminders within next ~1 hour
            if 0 <= diff_minutes <= 70:
                reminders.append(generate_reminder_message(appt))

        except:
            continue

    if not reminders:
        return "No reminders within the next hour.", format_all_appointments()

    return "\n\n".join(reminders), format_all_appointments()

# ================= UI =================

with gr.Blocks() as demo:
    gr.Markdown("## Appointment Reminder Manager")

    title = gr.Textbox(label="Appointment Title")
    date = gr.Textbox(label="Date (YYYY-MM-DD)")
    time = gr.Textbox(label="Time (HH:MM)")
    location = gr.Textbox(label="Location")
    notes = gr.Textbox(label="Notes")

    output = gr.Textbox(label="System Output")
    all_appts = gr.Textbox(label="All Appointments", lines=10)

    add_btn = gr.Button("Store Appointment")
    check_btn = gr.Button("Check 1 Hour Reminders")

    add_btn.click(
        add_appointment,
        inputs=[title, date, time, location, notes],
        outputs=[output, all_appts]
    )

    check_btn.click(
        check_one_hour_reminders,
        outputs=[output, all_appts]
    )

demo.launch(debug=True, share=True)
