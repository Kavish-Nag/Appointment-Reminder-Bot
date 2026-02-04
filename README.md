# Appointment-Reminder-Bot

A simple web based appointment reminder system built using **Python**, **Gradio**, and the **Scaledown API**.
This project allows users to store multiple appointments, prevent duplicates, automatically remove past events, and check reminders for upcoming appointments within about one hour.

---

## Features

* Store multiple appointments easily
* Prevent duplicate entries automatically
* Auto delete past appointments
* Check reminders for upcoming events within about 1 hour
* Display all saved appointments live
* Hidden internal assistant logic
* Lightweight Gradio web interface

---

## Tech Stack

* Python
* Gradio UI
* Requests
* Datetime
* Scaledown API

---

## How It Works

1. User enters appointment details such as title, date, time, location, and notes.
2. The system compresses internal context using the API.
3. Appointments are stored in memory.
4. Past appointments are automatically removed during operations.
5. When checking reminders, the system lists all upcoming appointments occurring soon.

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/appointment-reminder-manager.git
cd appointment-reminder-manager
```

### 2. Install dependencies

```
pip install gradio requests
```

### 3. Add API Key

If using Google Colab secrets:

```
userdata.get('APK')
```

Otherwise replace it with:

```
API_KEY = "YOUR_API_KEY"
```

---

## Running the App

```
python app.py
```

Gradio will launch a local interface and provide a public share link.

---

## Usage

1. Enter appointment information.
2. Click **Store Appointment** to save.
3. Click **Check 1 Hour Reminders** to see upcoming reminders.
4. The right panel always displays all stored appointments.

---

## Reminder Logic

The system checks for appointments occurring roughly within the next 0 to 70 minutes.

* Multiple reminders appear together if multiple appointments are upcoming.
* Past appointments are removed automatically.
* Duplicate appointments are blocked using a unique key check.

---

---

## Future Improvements

* Persistent storage using JSON or SQLite
* Automatic background reminder checks
* Table based UI instead of textbox list
* Notification integration

---
