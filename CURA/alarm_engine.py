import threading
import time
import sys
import pyttsx3
import json
import os
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────
# THREAD-SAFE AUDIO STRUCTURAL LOCK (Forces Queueing)
# ─────────────────────────────────────────────
_audio_lock = threading.Lock()

def _safe_speak_executor(text: str):
    with _audio_lock:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 145)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            del engine 
        except Exception as e:
            print(f"[TTS Driver Error]: {e}")

def speak(text: str):
    print(f"[CURA]: {text}")
    threading.Thread(target=_safe_speak_executor, args=(text,), daemon=True).start()

def play_beep(times: int = 3, frequency: int = 880, duration_ms: int = 400):
    for _ in range(times):
        try:
            if sys.platform == "win32":
                import winsound
                winsound.Beep(frequency, duration_ms)
            else:
                print("\a", end="", flush=True)
        except:
            pass
        time.sleep(0.15)

def play_medicine_alarm():
    play_beep(times=3, frequency=600, duration_ms=350)
    time.sleep(0.2)
    play_beep(times=4, frequency=880, duration_ms=400)


# ─────────────────────────────────────────────
# CURA URGENT INTEGRATED NOTIFICATION UTILITIES
# ─────────────────────────────────────────────
def trigger_emergency_alerts_isolated(medicine_name, missed_time):
    """
    Background automated alerts execution node targeting mail box and whatsapp chat.
    """
    config_file = 'data/patient.json' 
    receiver_email = "fazilkareem791@gmail.com"
    to_number = "+923431232577"
    whatsapp_on = True
    email_on = True
    patient_name = "Patient"

    # Loading dashboard forms settings dynamically if the file exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                c_data = json.load(f)
                receiver_email = c_data.get("email", receiver_email)
                to_number = c_data.get("whatsapp", to_number)
                whatsapp_on = c_data.get("whatsapp_on", whatsapp_on)
                email_on = c_data.get("email_on", email_on)
                patient_name = c_data.get("name", patient_name)
        except:
            pass

    #  EMAIL DISPATCH EXECUTION BLOCK
    if email_on:
        print(f"[DEBUG AUTOMATION] Dispatching Emergency Mail -> {receiver_email}")
        SENDER_EMAIL = "kayancyberlife@gmail.com"          
        SENDER_PASSWORD = "nneu djba idmk yklq" 

        subject = "CRITICAL ALERT: Medicine Missed for Patient!"
        body = f"Assalam o Alaikum,\n\nEmergency alert from CURA Health monitor.\n\nPatient ({patient_name}) have missed their scheduled medicine and no response received.\n\n📋 Medicine Details:\n- Name: {medicine_name}\n- Scheduled Time: {missed_time}\n- Alert Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nKindly check patient right now.\n\nRegards,\nCura Automated System"

        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = str(receiver_email).strip()  
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, str(receiver_email).strip(), msg.as_string())
            server.quit()
            print(f"[SYSTEM EMAIL]: Alert Dispatched Successfully to {receiver_email}")
        except Exception as mail_err:
            print(f" [SYSTEM EMAIL FAILURE]: {str(mail_err)}")

    #  WHATSAPP ULTRAMSG DISPATCH EXECUTION BLOCK
    if whatsapp_on:
        print(f"[DEBUG AUTOMATION] Dispatching Emergency WhatsApp -> {to_number}")
        INSTANCE_ID = "instance182816"
        TOKEN = "od8pxnfy5ka43vby"
        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

        message_body = (
            f" *CRITICAL ALERT: CURA Health Monitor*\n\n"
            f"Patient (*{patient_name}*) have missed their scheduled medicine and no response received.\n\n"
            f" *Medicine Details:*\n"
            f"- *Name:* {medicine_name}\n"
            f"- *Time:* {missed_time}\n"
            f"- *Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Kindly check patient right now."
        )

        try:
            clean_number = str(to_number).strip().replace("+", "").replace(" ", "").replace("-", "")
            payload = {
                "token": TOKEN,
                "to": clean_number,
                "body": message_body,
                "priority": 10
            }
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(url, data=payload, headers=headers, timeout=15)
            res_json = response.json()
            
            if "id" in res_json or res_json.get("sent") == "true" or res_json.get("sent") is True:
                print(f"[SYSTEM WHATSAPP]: Alert Dispatched Successfully to {clean_number}!")
            else:
                print(f" [SYSTEM WHATSAPP GATEWAY ERROR]: {res_json}")
        except Exception as wa_err:
            print(f"[SYSTEM WHATSAPP EXCEPTION]: {str(wa_err)}")


# ─────────────────────────────────────────────
# REAL-TIME PARALLEL PROCESS TRACKER
# ─────────────────────────────────────────────
def process_single_medicine_flow(patient_data: dict, med: dict):
    # Dynamic runtime lookup for name sync stability
    config_file = 'data/patient.json'
    patient_name = patient_data.get('name', 'Patient')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                patient_name = json.load(f).get("name", patient_name)
        except:
            pass

    med_name     = med.get('name', 'medicine')
    med_dose     = med.get('dose', med.get('dosage', '1 tablet'))
    med_time     = med.get('time', '')

    print(f"\n[ALARM ACTIVE] Thread launched successfully for: {med_name} at {med_time}")
    
    play_medicine_alarm()
    
    speak(f"{patient_name}, it is time to take your {med_name}!")
    time.sleep(1.5)
    speak(f"Your dose is {med_dose}. Please update your status on the dashboard.")

    start_time = time.time()
    deadline = start_time + 300   
    schedule_file = 'data/schedule.json'

    while time.time() < deadline:
        is_taken_via_ui = False
        if os.path.exists(schedule_file):
            try:
                with open(schedule_file, 'r') as sf:
                    meds_list = json.load(sf)
                for m in meds_list:
                    if m.get('name') == med_name and m.get('time') == med_time:
                        if m.get('status') == 'Taken':
                            is_taken_via_ui = True
                            break
            except:
                pass

        if is_taken_via_ui:
            print(f" [SUCCESS] {med_name} was marked as TAKEN via Dashboard.")
            return

        time.sleep(2)

    # TIMEOUT LOGIC
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, 'r') as sf:
                meds_list = json.load(sf)
            for m in meds_list:
                if m.get('name') == med_name and m.get('time') == med_time:
                    if m['status'] != 'Taken':
                        m['status'] = 'Missed'
            with open(schedule_file, 'w') as sf:
                json.dump(meds_list, sf, indent=4)
            print(f" [TIMEOUT] 5 minutes elapsed. {med_name} marked as Missed.")
            speak(f"Alert! {med_name} has been marked as missed.")
            
            # CALL INJECTION: Triggering integrated email and WhatsApp alert instantly
            trigger_emergency_alerts_isolated(med_name, med_time)
            
        except Exception as e:
            print(f"[JSON Write Error]: {e}")

# ─────────────────────────────────────────────
# AUTOMATION ENGINE LOOP (NON-BLOCKING CORE)
# ─────────────────────────────────────────────
def monitor_schedule_and_alert():
    print("\n============================================================")
    print(" CURA LIVE ENGINE ACTIVE: CRASH-PROOF SCHEDULER MODE")
    print("============================================================\n")

    triggered_cache = set()
    last_checked_minute = ""

    while True:
        schedule_file = 'data/schedule.json'
        config_file = 'data/patient.json'
        
        # Load identity from JSON dynamically to match dashboard forms state
        current_patient = {"name": "Patient", "age": 21}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    c_data = json.load(f)
                    current_patient["name"] = c_data.get("name", "Patient")
                    current_patient["age"] = c_data.get("age", 21)
            except:
                pass
        
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")

        if current_time_str != last_checked_minute:
            triggered_cache.clear()
            last_checked_minute = current_time_str

        if os.path.exists(schedule_file):
            try:
                with open(schedule_file, 'r') as sf:
                    meds_list = json.load(sf)
            except:
                meds_list = []

            for med in meds_list:
                med_name = med.get('name', '')
                med_time_short = med.get('time', '')[:5]
                cache_key = f"{med_name}_{med_time_short}"

                if med_time_short == current_time_str and med.get('status') == 'Pending':
                    if cache_key not in triggered_cache:
                        print(f"\n TIME MATCH HIT: Executing reminder thread for '{med_name}' at {current_time_str}")
                        triggered_cache.add(cache_key)
                        
                        threading.Thread(
                            target=process_single_medicine_flow, 
                            args=(current_patient, med), 
                            daemon=True
                        ).start()

        time.sleep(1)

if __name__ == "__main__":
    monitor_schedule_and_alert()