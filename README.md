#  CURA: AI-Powered Automated Medication Compliance and Patient Alert System

CURA is an intelligent, medication tracking framework designed to help elderly patients adhere to their daily prescription schedules while providing real-time compliance tracking for family guardians. 

Built using Python, Streamlit, OpenCV, Text-to-Speech (TTS), and Gemini AI, the system actively calls out medicine reminders, captures live webcam feeds to inspect medicine packaging, verifies medicine identity using multimodal AI, and updates a centralized status log.

---

##  Key Features

*  Automated Spoken Reminders: Uses Text-to-Speech (TTS) to announce natural voice reminders specifying patient name, medicine, and exact dosage.
*  Live Webcam Scan: Integrates OpenCV to capture medicine bottles or strips shown by the patient.
*  Multimodal AI Verification: Leverages AI to analyze captured images against prescribed schedules.
*  Guardian Compliance Dashboard: Real-time Streamlit interface displaying Taken, Pending, and Missed logs.
*  Privacy-First Architecture: Video frames and logs are processed locally without exposing indoor continuous video feeds publicly.

---

##  Tech Stack & Dependencies

* Language: Python 3.10+
* Frontend / UI: Streamlit
* Computer Vision: OpenCV (opencv-python)
* Artificial Intelligence: Google Gemini API (google-genai)
* Audio Synthesizer: Pyttsx3 / gTTS
* Data Processing: Pandas / NumPy

---

##  Quick Start Guide

### 1. Prerequisites
Ensure you have Python installed on your system:
python --version

### 2. Clone the Repository
git clone https://github.com/YOUR-USERNAME/CURA-AI-Medication-Tracker.git
cd CURA-AI-Medication-Tracker

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Set Up Environment Variables
Set your Gemini API Key in your terminal or environment:

Windows (Command Prompt):
set GEMINI_API_KEY="your_api_key_here"

Linux/Mac:
export GEMINI_API_KEY="your_api_key_here"

### 5. Run the Application
streamlit run app.py

---

##  Project Structure

CURA
├
data/
├── .env                     # API_KEY storage
├── alarm_engine.py          # alerts and alarm
├── alerts_engine.py         # alerts and hazard flag
├── app.py                   # Main Streamlit application entry point
├── reminder.py              # Medicine scheduale mannagment
├── security.py.py           # for string pass
├── requirements.txt         # List of Python dependencies
├── README.md                # Project documentation
└── assets/ ![CURA Dashboard](assets/dashboard.png)                 # UI screenshots and flowcharts

---

##  Future Roadmap (IoT Hardware Transition)

The current PC-based MVP is designed to transition into a dedicated standalone IoT device:
* Microcontroller: Raspberry Pi Zero 2 W with a custom 3D-printed enclosure.
* Edge Computing: Local SQLite caching for offline speech generation during internet breakdown.
* Emergency Routing: Integration with WhatsApp API for automated guardian alerts on missed doses.

---

##  Academic Context
This project was developed as an Academic AI Project by Hamza Kayani at Hamdard University, Karachi (Department of Cyber Security and Digital Forensics).

---

##  License
This project is open-source and available under the MIT License.
