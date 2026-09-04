
import json
import time
import schedule
from datetime import datetime
from data import run_full_reminder_flow
from data  import speak

# ─────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────

def load_patients() -> list:
    """patients.json se sab patients load karo"""
    try:
        with open("data/patients.json", "r") as f:
            return json.load(f).get("patients", [])
    except FileNotFoundError:
        print("[ERROR] data/patients.json nahi mili!")
        return []

# ─────────────────────────────────────────────
# SCHEDULE SETUP
# ─────────────────────────────────────────────

def _make_job(patient: dict, medicine: dict):
    
    def job():
        now = datetime.now().strftime("%I:%M %p")
        print(f"\n[{now}] Reminder triggered: {patient['name']} → {medicine['name']}")
        run_full_reminder_flow(patient, medicine)
    return job


def setup_all_reminders():

    patients = load_patients()

    if not patients:
        speak("No patient registered first add patient from dashboard.")
        return

    count = 0
    for patient in patients:
        for medicine in patient.get("medicines", []):
            med_time = medicine.get("time", "")
            if not med_time:
                continue

            schedule.every().day.at(med_time).do(
                _make_job(patient, medicine)
            )

            print(f"[Scheduled] {patient['name']} — {medicine['name']} at {med_time}")
            count += 1

    speak(
        f"CURA is ready. {len(patients)} for patient  "
        f"{count} medicine reminders is set."
    )


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

def run_reminders():
    """
    Reminder systems main loop.
    main.py is calling in beckground.
    """
    setup_all_reminders()
    while True:
        schedule.run_pending()
        time.sleep(20)   


# ─────────────────────────────────────────────
# TEST MODE
# python core/reminder.py
# ─────────────────────────────────────────────
if __name__ == "__main__":
    from datetime import datetime, timedelta

    print("[TEST MODE] Ek minute baad reminder fire hoga...")

    # Aaj ka time + 1 minute
    test_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")

    test_patient  = {
        "name": "Dada Jan",
        "age": 72,
        "emergency_contact": "+923001234567",
        "emergency_email": "family@gmail.com",
        "medicines": [{"name": "Metformin 500mg", "time": test_time, "dose": "1 tablet"}]
    }
    test_medicine = test_patient["medicines"][0]

    schedule.every().day.at(test_time).do(
        _make_job(test_patient, test_medicine)
    )

    print(f"[TEST] Reminder set for {test_time}. Wait kar rahe hain...")

    while True:
        schedule.run_pending()
        time.sleep(10)
