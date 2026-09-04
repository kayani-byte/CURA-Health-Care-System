import os
import json
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────
# CURA EMERGENCY NOTIFICATION ENGINE (EMAIL)
# ─────────────────────────────────────────────
def send_emergency_email(receiver_email, medicine_name, missed_time):
    """
    Gmail sends Alert mails to family members Via SMTP Server dynamically.
    """
    print(f"\n[DEBUG EMAIL] Target Email: {receiver_email} | Med: {medicine_name}")
    
    # CONFIGURATION
    SENDER_EMAIL = "sender here"          
    SENDER_PASSWORD = "password here" 

    subject = "⚠️ CRITICAL ALERT: Medicine Missed for Patient!"
    body = f"""
    Assalam o Alaikum,

    Emergency alert from CURA Health monitor.
    
    Patient have missed their scheduled medicine and no response received.
    
     Medicine Details:
    - Name: {medicine_name}
    - Scheduled Time: {missed_time}
    - Alert Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Kindly check patient right now.
    
    Regards,
    Cura Automated System
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = str(receiver_email).strip()  
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        print("[DEBUG EMAIL] Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("[DEBUG EMAIL] Attempting login...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print("[DEBUG EMAIL] Sending message...")
        server.sendmail(SENDER_EMAIL, str(receiver_email).strip(), msg.as_string())
        server.quit()
        
        print(f" [DEBUG EMAIL] Email Sent Successfully to {receiver_email}")
        return True
    except Exception as e:
        print(f" [DEBUG EMAIL] Exception Caught: {str(e)}")
        return False


# ─────────────────────────────────────────────
# CURA EMERGENCY NOTIFICATION ENGINE (WHATSAPP)
# ─────────────────────────────────────────────
def send_emergency_whatsapp(to_number, medicine_name, missed_time):
    """
    UltraMsg API sends direvt Alearts to members.
    """
    print(f"\n[DEBUG WA] Target Number: {to_number} | Med: {medicine_name}")
    
    # ULTRAMSG CONFIGURATION 
    INSTANCE_ID = "HERE"
    TOKEN = "HERE"
    
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

    message_body = (
        f" *CRITICAL ALERT: CURA Health Monitor*\n\n"
        f"Patient have missed their scheduled medicine and no response received.\n\n"
        f" *Medicine Details:*\n"
        f"- *Name:* {medicine_name}\n"
        f"- *Time:* {missed_time}\n"
        f"- *Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Kindly check patient right now."
    )

    try:
        clean_number = str(to_number).strip().replace("+", "").replace(" ", "").replace("-", "")
        print(f"[DEBUG WA] Cleaned Number for Payload: {clean_number}")
        
        payload = {
            "token": TOKEN,
            "to": clean_number,
            "body": message_body,
            "priority": 10
        }
        
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        print(f"[DEBUG WA] Sending HTTP POST request to UltraMsg...")
        
        response = requests.post(url, data=payload, headers=headers, timeout=12)
        print(f"[DEBUG WA] Response Status Code: {response.status_code}")
        
        res_json = response.json()
        print(f"[DEBUG WA] Raw API Response JSON: {res_json}")
        
        if "id" in res_json or res_json.get("sent") == "true" or res_json.get("sent") is True:
            print(f" [DEBUG WA] WhatsApp Alert Sent Successfully to {clean_number}!")
            return True
        else:
            print(f" [DEBUG WA] UltraMsg Logic Failed. Response structure unexpected.")
            return False
            
    except Exception as e:
        print(f"[DEBUG WA] Exception Caught: {str(e)}")
        return False