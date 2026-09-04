import streamlit as st
import json
import os
import datetime
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
from security import hash_password, is_strong_password, verify_password
from alerts_engine import send_emergency_email, send_emergency_whatsapp

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CURA — Elderly Care",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# VALIDATE SCHEDULE TIMES (ROBUST & CLEANED)
# ─────────────────────────────────────────────
def validate_schedule_times():
    SCHEDULE_FILE = "data/schedule.json"
    
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r") as f:
                schedule_data = json.load(f)
        except Exception as e:
            print(f"[Cura Loop Error]: schedule.json read failed -> {e}")
            return

        updated = False
        now = datetime.now()
        
        # Exact 5 minutes dynamic configuration
        timeout_mins = 5
        for med in schedule_data:
            if med.get("status") == "Pending":
                try:
                    med_time = datetime.strptime(med["time"], "%H:%M:%S").time()
                    med_datetime = datetime.combine(now.date(), med_time)
                    
                    # Agar time exact 5 minutes guzar chuka hai, mark as Missed
                    if now > (med_datetime + timedelta(minutes=timeout_mins)):
                        med["status"] = "Missed"
                        updated = True
                        print(f"⚠️ [CURA System]: {med.get('name')} marked as Missed after 5 mins threshold.")
                except Exception:
                    continue
                    
        # File update logic and runtime synchronization
        if updated:
            with open(SCHEDULE_FILE, "w") as f:
                json.dump(schedule_data, f, indent=4)
            
            # Safe Streamlit reload implementation
            try:
                import streamlit as st
                st.rerun()
            except ImportError:
                print("[Cura UI Warning]: Streamlit context not found, skipped reload sync.")
            except Exception:
                pass
# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
def apply_cura_styles():
    # Fonts + FontAwesome loaded via markdown (external links only, no CSS here)
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>'
        '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700'
        '&family=DM+Serif+Display&display=swap" rel="stylesheet"/>',
        unsafe_allow_html=True,
    )

    # All CSS injected through a dedicated style block — no special Unicode chars inside
    css = """
<style>
:root {
    --blue-lightest: #E3F2FD;
    --blue-light: #BBDEFB;
    --blue-mid: #64B5F6;
    --blue-brand: #1976D2;
    --blue-deep: #0D47A1;
    --blue-ink: #0A3880;
    --white: #FFFFFF;
    --surface: #F7FAFD;
    --border: #DCE8F5;
    --text-primary: #0D2B5E;
    --text-secondary: #4A6B8A;
    --text-muted: #89A4BF;
    --green: #2E7D32;
    --green-light: #E8F5E9;
    --red: #C62828;
    --red-light: #FFEBEE;
    --amber: #E65100;
    --amber-light: #FFF3E0;
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-pill: 999px;
    --shadow-sm: 0 2px 8px rgba(13,71,161,.07);
    --shadow-md: 0 4px 20px rgba(13,71,161,.11);
    --font-body: 'DM Sans', sans-serif;
    --font-display: 'DM Serif Display', serif;
}

html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    color: var(--text-primary);
}

.main .block-container {
    background: var(--surface);
    padding: 2rem 2.5rem 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, var(--blue-deep) 0%, var(--blue-ink) 100%) !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #fff !important;
    border-radius: var(--radius-pill) !important;
    font-weight: 600 !important;
    width: 100%;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.25) !important;
}

.cura-logo {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 2px solid var(--border);
}

.cura-logo-icon {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, var(--blue-brand), var(--blue-deep));
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-md);
}

.cura-logo-icon i {
    font-size: 1.5rem;
    color: #fff;
}

.cura-logo-text .logo-title {
    font-family: var(--font-display);
    font-size: 2rem;
    color: var(--blue-deep);
}

.stButton > button {
    border-radius: var(--radius-pill) !important;
    background: linear-gradient(135deg, var(--blue-brand) 0%, var(--blue-deep) 100%) !important;
    color: #fff !important;
    font-weight: 600 !important;
}

.stat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.5rem;
    box-shadow: var(--shadow-sm);
}

.stat-card .stat-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: .06em;
    margin-bottom: .3rem;
}

.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--blue-deep);
}

.stat-card .stat-sub {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: .2rem;
}

.section-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.5rem;
}

.section-card h3 {
    margin-top: 0;
    color: var(--blue-deep);
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    font-size: .75rem;
    font-weight: 600;
}

.badge-pending { background: var(--amber-light); color: var(--amber); }
.badge-taken   { background: var(--green-light);  color: var(--green); }
.badge-missed  { background: var(--red-light);    color: var(--red);   }

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* header hide nahi karna — sidebar toggle usi mein hota hai */
/* header { visibility: hidden; } */

/* Sidebar toggle button hamesha visible aur styled rahe */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    background: linear-gradient(135deg, #1976D2, #0D47A1) !important;
    border-radius: 0 8px 8px 0 !important;
    color: #fff !important;
}

[data-testid="collapsedControl"] svg {
    fill: #ffffff !important;
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOGO HELPERS
# ─────────────────────────────────────────────
def cura_logo(subtitle: str = "Elderly Care Dashboard") -> None:
    st.markdown(
        f"""
        <div class="cura-logo">
            <div class="cura-logo-icon"><i class="fa-solid fa-heart-pulse"></i></div>
            <div class="cura-logo-text">
                <span class="logo-title">Cura</span><br>
                <span style="color:#89A4BF;font-size:.8rem;text-transform:uppercase;">{subtitle}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cura_sidebar_logo() -> None:
    st.sidebar.markdown(
        """
        <div class="cura-logo" style="border-bottom:1px solid rgba(255,255,255,0.2)">
            <div class="cura-logo-icon"><i class="fa-solid fa-heart-pulse"></i></div>
            <div class="cura-logo-text">
                <span class="logo-title" style="color:white!important;">Cura</span><br>
                <span style="font-size:.7rem;color:rgba(255,255,255,.55)!important;text-transform:uppercase;">Elderly Care System</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────
DATA_DIR      = "data"
PROFILE_FILE  = f"{DATA_DIR}/profile.json"
SCHEDULE_FILE = f"{DATA_DIR}/schedule.json"
PATIENT_FILE  = f"{DATA_DIR}/patient.json"
ALERTS_FILE   = f"{DATA_DIR}/alerts.json"


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(path: str, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default


def save_json(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_schedule() -> list:
    return load_json(SCHEDULE_FILE, [])


def load_patient() -> dict:
    return load_json(PATIENT_FILE, {})


def load_alerts() -> dict:
    return load_json(ALERTS_FILE, {"whatsapp": "", "email": "", "timeout_minutes": 5})


# ─────────────────────────────────────────────
# AUTH  — LOGIN / REGISTER
# ─────────────────────────────────────────────
def run_auth():
    account_exists = os.path.exists(PROFILE_FILE)
    cura_sidebar_logo()

    # ── Sidebar info ──────────────────────────────────────────
    if account_exists:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Secure Access")
        st.sidebar.info(
            "**Only one caretaker account** register at a time.\n\n"
            "For new registration first login to current account, then "
            "Remove current caretaker."
        )
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            "<small style='opacity:.7'>Account remove option "
            "is in dashboard option.</small>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown("---")
        st.sidebar.markdown("###  First time Setup")
        st.sidebar.warning(
            "No caretaker profile found.\n\n"
            "Down Below **Registration form** Fill it to CURA  "
            "activate ."
        )
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            "<small style='opacity:.7'>Registration ke baad "
            "automatically login screen khulegi.</small>",
            unsafe_allow_html=True,
        )

  # ── Main page — clean, minimalist ────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        cura_logo("Secure Access")

        if account_exists:
            st.subheader("Dashboard Login")
            user     = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button(" Login", key="btn_login", use_container_width=True):
                stored = load_json(PROFILE_FILE, {})
                if user == stored.get("username") and verify_password(stored.get("password", ""), password):
                    st.session_state["auth"] = True
                    st.session_state["page"] = "overview"
                    st.rerun()
                else:
                    st.error(" Username or password wrong.")
        else:
            st.subheader("Family Member Registration")
            new_user = st.text_input("Create Username", key="reg_user")
            # FIX: Changed invalid type="Create password" to type="password"
            new_pass = st.text_input("Create Password", type="password", key="reg_pass")

            if st.button(" Register Account", key="btn_register", use_container_width=True):
                if not new_user.strip() or not new_pass.strip():
                    st.error("No empty field allowed.")
                else:
                    strong, msg = is_strong_password(new_pass)
                    if strong:
                        save_json(PROFILE_FILE, {
                            "username": new_user,
                            "password": hash_password(new_pass),
                        })
                        st.success(" Registration Successfull! Login screen...")
                        st.rerun()
                    else:
                        st.error(msg)

# ─────────────────────────────────────────────
# DASHBOARD PAGES
# ─────────────────────────────────────────────

# ── Overview / Home (Clean & Automated Refresh Sync) ──────────────────────────
def page_overview():
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=5000, limit=None, key="cura_dashboard_refresher")

    validate_schedule_times()
    cura_logo("Patient Dashboard")

    schedule = load_schedule()
    patient  = load_patient()

    pending = sum(1 for m in schedule if m.get("status") == "Pending")
    taken   = sum(1 for m in schedule if m.get("status") == "Taken")
    missed  = sum(1 for m in schedule if m.get("status") == "Missed")
    total   = len(schedule)

    patient_name = patient.get("name", "Patient")

    # Welcome banner
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1976D2,#0D47A1);
                    border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.5rem;color:#fff;">
            <h2 style="margin:0;font-family:'DM Serif Display',serif;">
                Assalam o Alaikum 
            </h2>
            <p style="margin:.4rem 0 0;opacity:.85;">
                <b>Cura is active for {patient_name}.</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    def stat(col, icon, label, value, sub, color="#0D47A1"):
        with col:
            st.markdown(
                f"""<div class="stat-card">
                    <div class="stat-label"><i class="fa-solid {icon}"></i>&nbsp; {label}</div>
                    <div class="stat-value" style="color:{color};">{value}</div>
                    <div class="stat-sub">{sub}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    stat(c1, "fa-pills",        "Total Medicines", total,   "Scheduled",          "#0D47A1")
    stat(c2, "fa-clock",        "Pending",         pending, "Have to take",      "#E65100")
    stat(c3, "fa-circle-check", "Taken",           taken,   "Done",              "#2E7D32")
    stat(c4, "fa-triangle-exclamation", "Missed",  missed,  "No Response", "#C62828")

    st.markdown("<br>", unsafe_allow_html=True)

    # STRICT TIME-BOUND CURRENT DUE MEDICATIONS PANEL
    active_pending_meds = [m for m in schedule if m.get("status") == "Pending"]
    if active_pending_meds:
        st.markdown('<h4 style="color:#E65100;"><i class="fa-solid fa-hourglass-half"></i> Current Due Medications</h4>', unsafe_allow_html=True)
        
        from datetime import datetime
        now_str = datetime.now().strftime("%H:%M")
        
        for med in active_pending_meds:
            m_name = med.get("name")
            m_time = med.get("time")
            m_dose = med.get("dose", med.get("dosage", "1 tablet"))
            
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                st.markdown(f"🔹 **{m_name}** — {m_dose} scheduled at `{m_time}`")
            with col_m2:
                #  LOCK CONDITION: Current time matches or crosses scheduled time
                if now_str >= m_time:
                    if st.button(f"✓ Taken", key=f"take_{m_name}_{m_time}", use_container_width=True):
                        for item in schedule:
                            if item.get("name") == m_name and item.get("time") == m_time:
                                item["status"] = "Taken"
                        save_json(SCHEDULE_FILE, schedule)
                        st.success(f"{m_name} registered!")
                        st.rerun()
                else:
                    st.markdown(f"<div style='text-align:center;color:#777;font-size:0.85rem;padding-top:5px;'>🔒 Locked until {m_time}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # System Action Panel Grid
    st.markdown('<div class="section-card"><h3>⚙️ System Quick Panel</h3></div>', unsafe_allow_html=True)
    btn_c1, btn_c2 = st.columns(2)
    with btn_c1:
        if st.button(" Chat with Cura Bot", key="dash_chat_btn", use_container_width=True, type="primary"):
            st.session_state["page"] = "companion"
            st.rerun()
    with btn_c2:
        if st.button(" Open Camera / Scan Medicine", key="quick_cam", use_container_width=True):
            st.session_state["page"] = "camera"
            st.rerun()

    # Live Invisible Background Fragment Timer
    @st.fragment(run_every=10)
    def background_tracker():
        validate_schedule_times()

    background_tracker()


# ── Patient Profile ──────────────────────────
def page_patient():
    cura_logo("Patient Profile")
    patient = load_patient()

    st.markdown('<div class="section-card"><h3><i class="fa-solid fa-user-injured"></i> Patient Information</h3>', unsafe_allow_html=True)

    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input("Patient Name",   value=patient.get("name", ""))
            age   = st.number_input("Age",     value=int(patient.get("age", 65)), min_value=1, max_value=120)
            blood = st.text_input("Blood Group",       value=patient.get("blood", ""))
        with col2:
            phone     = st.text_input("Phone Number",          value=patient.get("phone", ""))
            condition = st.text_input("Disease / Condition",   value=patient.get("condition", ""))
            doctor    = st.text_input("Doctor Name",        value=patient.get("doctor", ""))

        st.markdown("**Emergency Contact**")
        col3, col4 = st.columns(2)
        with col3:
            em_name  = st.text_input("Emergency Contact Name",     value=patient.get("em_name", ""))
            em_phone = st.text_input("WhatsApp Number (+923...)",  value=patient.get("em_phone", ""))
        with col4:
            em_email = st.text_input("Emergency Email",            value=patient.get("em_email", ""))
            relation = st.text_input("Relation with patient",   value=patient.get("relation", ""))

        if st.form_submit_button(" Save profile", use_container_width=True):
            save_json(PATIENT_FILE, {
                "name": name, "age": age, "blood": blood,
                "phone": phone, "condition": condition, "doctor": doctor,
                "em_name": em_name, "em_phone": em_phone,
                "em_email": em_email, "relation": relation,
            })
            st.success(" Patient profile saved")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Show current profile
    if patient:
        st.markdown('<div class="section-card"><h3><i class="fa-solid fa-id-card"></i> Current Profile</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name",      patient.get("name", "—"))
            st.metric("Age",      f"{patient.get('age', '—')} saal")
        with col2:
            st.metric("Blood",     patient.get("blood", "—"))
            st.metric("Doctor",    patient.get("doctor", "—"))
        with col3:
            st.metric("Emergency", patient.get("em_name", "—"))
            st.metric("WhatsApp",  patient.get("em_phone", "—"))
        st.markdown('</div>', unsafe_allow_html=True)


# ── Medicine Schedule ────────────────────────
def page_schedule():
    validate_schedule_times()

    cura_logo("Medicine Schedule")
    schedule = load_schedule()

    # Add form
    st.markdown('<div class="section-card"><h3><i class="fa-solid fa-plus-circle"></i> ADD Medicine</h3>', unsafe_allow_html=True)
    with st.form("med_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            med_name   = st.text_input("Medicine name")
        with col2:
            med_time   = st.time_input("Reminder Time", step=timedelta(minutes=1))
        with col3:
            med_dosage = st.text_input("Dosage (e.g. 1 Tablet)")

        if st.form_submit_button("➕ Add Medicine", use_container_width=True):
            if not med_name.strip():
                st.error("Medicine name.")
            else:
                schedule.append({
                    "name": med_name, "time": str(med_time),
                    "dosage": med_dosage, "status": "Pending"
                })
                save_json(SCHEDULE_FILE, schedule)
                st.success(f" {med_name} Aded in schedule ")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Display table
    st.markdown('<div class="section-card"><h3><i class="fa-solid fa-list-check"></i> Current Schedule</h3>', unsafe_allow_html=True)
    if not schedule:
        st.info("No Medicine schedualed. Fill the above form to add.")
    else:
        h1, h2, h3, h4, h5, h6 = st.columns([3, 2, 2, 2, 2, 2])
        for col, label in zip([h1,h2,h3,h4,h5,h6], ["**Name**","**Time**","**Dosage**","**Status**","**Mark**","**Remove**"]):
            col.markdown(label)
        st.markdown("---")

        for idx, med in enumerate(schedule):
            c1,c2,c3,c4,c5,c6 = st.columns([3,2,2,2,2,2])
            c1.write(med["name"])
            c2.write(med["time"])
            c3.write(med["dosage"])

            status = med.get("status", "Pending")
            badge_class = {"Pending":"badge-pending","Taken":"badge-taken","Missed":"badge-missed"}.get(status,"badge-pending")
            c4.markdown(f'<span class="badge {badge_class}">{status}</span>', unsafe_allow_html=True)

            with c5:
                new_status = st.selectbox("", ["Pending","Taken","Missed"],
                                          index=["Pending","Taken","Missed"].index(status),
                                          key=f"status_{idx}", label_visibility="collapsed")
                if new_status != status:
                    schedule[idx]["status"] = new_status
                    save_json(SCHEDULE_FILE, schedule)
                    st.rerun()

            with c6:
                if st.button("", key=f"del_{idx}"):
                    schedule.pop(idx)
                    save_json(SCHEDULE_FILE, schedule)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# ── AI Chat Companion────────
# ==============================================================================
def page_companion():
    cura_logo("AI chat Companion")

    if st.button(" Go to Overview Dashboard", key="go_to_overview_dash", type="secondary"):
        st.session_state["page"] = "Dashboard"  
        st.rerun()

    st.markdown(
        """
        <div class="section-card">
            <h3><i class="fa-solid fa-microphone-lines"></i> AI chat Companion Profile Settings</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    companion_file = f"{DATA_DIR}/companion.json"
    companion = load_json(companion_file, {
        "language": "Urdu + English",
        "tone": "Warm and Friendly",
        "topics": "Health, Motivation, General chat",
        "exit_word": "Good Bye",
    })

    with st.form("companion_form"):
        col1, col2 = st.columns(2)
        with col1:
            language  = st.selectbox("Language Configuration", ["Urdu + English","Urdu Only","English Only"],
                                     index=["Urdu + English","Urdu Only","English Only"].index(companion.get("language","Urdu + English")))
            tone      = st.selectbox("Personality Tone", ["Warm and Friendly","Professional","Simple and Slow"],
                                     index=["Warm and Friendly","Professional","Simple and Slow"].index(companion.get("tone","Warm and Friendly")))
        with col2:
            topics    = st.text_input("Allowed Knowledge Boundaries",  value=companion.get("topics",""))
            exit_word = st.text_input("Termination Command", value=companion.get("exit_word","khuda hafiz"))

        if st.form_submit_button(" Save Profile Configuration", use_container_width=True):
            save_json(companion_file, {"language":language,"tone":tone,"topics":topics,"exit_word":exit_word})
            st.success("AI configurations saved successfully!")
            st.rerun()

    # ── LIVE BOT CHAT REGISTRY WINDOW ───────────────────
    st.markdown("---")
    st.subheader(" Interactive Assistant Logs")

    if "companion_chat_history" not in st.session_state:
        st.session_state.companion_chat_history = []

    # Predefined Clickable Pills Questions
    st.write(" **Quick Questions:**")
    p1, p2, p3 = st.columns(3)
    clicked_query = None
    
    with p1:
        if st.button(" What is my current scheduale?", key="p_sched", use_container_width=True):
            clicked_query = "Tell me my todays scheduale and medicine."
    with p2:
        if st.button(" Which medicine did i miss today?", key="p_miss", use_container_width=True):
            clicked_query = "Did i miss any medicine?"
    with p3:
        if st.button("Health Tips & Precautions", key="p_health", use_container_width=True):
            clicked_query = "Elderly health care ke liye kuch quick tips ya precautions batayein."

    user_chat_input = st.chat_input("Cura se yahan direct baat karein...")
    if clicked_query:
        user_chat_input = clicked_query

    # Fixed height scrollable window container
    chat_container = st.container(height=380, border=True)
    
    with chat_container:
        for msg in st.session_state.companion_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if user_chat_input:
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_chat_input)
        st.session_state.companion_chat_history.append({"role": "user", "content": user_chat_input})

        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        load_dotenv(override=True)
        
        # Keys load karne ka framework
        api_keys = [
            os.getenv("GEMINI_KEY_1"),
            os.getenv("GEMINI_KEY_2"),
            os.getenv("GEMINI_KEY_3")
        ]
        api_keys = [k for k in api_keys if k]

        if not api_keys:
            with chat_container:
                with st.chat_message("assistant"):
                    st.error("Error: Did not find any GEMINI_KEY in .env file .")
        else:
            schedule = load_schedule()
            patient  = load_patient()
            patient_name = patient.get("name", "Patient")
            
            system_instruction = (
                f"You are Cura, an advanced AI medical care companion software.\n"
                f"The patient name is {patient_name}.\n"
                f"Current Live Schedule Data: {str(schedule)}.\n"
                f"Talk strictly in Roman Urdu (if user talks in Urdu) or simple English.\n"
                f"Language mode selected: {language}, Tone setting: {tone}.\n"
                f"Use the schedule data to accurately reply which medication is Taken, Pending, or Missed. Keep answers extremely short and human-written."
            )
            
            reply_text = None
            
            # Key Rotation Loop for Chatbot
            for current_key in api_keys:
                try:
                    genai.configure(api_key=current_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        system_instruction=system_instruction
                    )
                    response = model.generate_content(user_chat_input)
                    reply_text = response.text
                    if reply_text:
                        break
                except Exception as e:
                    if "429" in str(e) or "quota" in str(e).lower():
                        continue
                    else:
                        try:
                            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                            full_combined_prompt = f"{system_instruction}\n\nUser Question: {user_chat_input}"
                            response = model.generate_content(full_combined_prompt)
                            reply_text = response.text
                            if reply_text:
                                break
                        except:
                            continue

            if reply_text:
                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(reply_text)
                st.session_state.companion_chat_history.append({"role": "assistant", "content": reply_text})
                st.rerun()
            else:
                with chat_container:
                    with st.chat_message("assistant"):
                        st.error("All API Keys quota is full, wait for a while.")


# ==============================================================================
# ── CAMERA MEDICINE VERIFY (With Multi-Key Rotation Integration) ──────────────
# ==============================================================================
def page_camera():
    import google.generativeai as genai 
    from PIL import Image
    import json
    import os
    from dotenv import load_dotenv

    load_dotenv(override=True)
    
    # Camera panel ke liye bhi same rotation keys extraction
    api_keys = [
        os.getenv("GEMINI_KEY_1"),
        os.getenv("GEMINI_KEY_2"),
        os.getenv("GEMINI_KEY_3")
    ]
    api_keys = [k for k in api_keys if k]

    cura_logo("Medicine Verification")

    st.markdown(
        """
        <div class="section-card">
            <h3><i class="fa-solid fa-camera"></i> Camera-Based Medicine Verification</h3>
            <p>Patient show medicine strip in camera and it detect and matches with scheduale.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="section-card" style="min-height:200px;">
                <h3><i class="fa-solid fa-list"></i> Kaise Kaam Karta Hai?</h3>
                <ol style="color:var(--text-secondary);line-height:2;">
                    <li>Patient place the medicine in front of camera </li>
                    <li>OpenCV captures the image</li>
                    <li>Gemini Vision API identifies medicines</li>
                    <li>Compares with scheduale</li>
                    <li>CURA says: right or wrong</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="section-card" style="min-height:200px;">
                <h3><i class="fa-solid fa-terminal"></i> How to verify?</h3>
                <p style="color:var(--text-secondary);">Run this command in terminal :</p>
                <code style="background:#E3F2FD;padding:8px 12px;border-radius:8px;display:block;margin-bottom:1rem;">
                    python core/medicine_verify.py
                </code>
                <p style="color:var(--text-secondary);">Ya main CURA system se:</p>
                <code style="background:#E3F2FD;padding:8px 12px;border-radius:8px;display:block;">
                    python main.py
                </code>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card"><h3> Scan Your Medicine</h3>', unsafe_allow_html=True)
    
    img_file = st.camera_input("Take a clear picture of the medicine label")

    if img_file is not None:
        with st.spinner(" Scanning medicine strip and verifying with schedule..."):
            os.makedirs("data", exist_ok=True)
            img_path = "data/captured_med.jpg"
            
            image = Image.open(img_file)
            image.save(img_path)
            
            scanned_med_name = "Unknown"
            prompt = "Read the medicine name from this image. Output ONLY the medicine name, nothing else. If you can't read it clearly, output 'Unknown'."
            
            if not api_keys:
                st.error("Error: Keys config missing in .env")
                scanned_med_name = "Error reading API"
            else:
                # Key Rotation Loop for Camera Scanner
                for current_key in api_keys:
                    try:
                        genai.configure(api_key=current_key)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content([prompt, image])
                        scanned_med_name = response.text.strip()
                        if scanned_med_name and "Error" not in scanned_med_name:
                            break
                    except Exception as e:
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            response = model.generate_content([prompt, image])
                            scanned_med_name = response.text.strip()
                            if scanned_med_name and "Error" not in scanned_med_name:
                                break
                        except:
                            continue

            st.info(f" Scanned Medicine Name: **{scanned_med_name}**")

            SCHEDULE_FILE = "data/schedule.json"
            match_found = False
            
            if os.path.exists(SCHEDULE_FILE) and scanned_med_name != "Error reading API" and scanned_med_name != "Unknown":
                try:
                    with open(SCHEDULE_FILE, "r") as f:
                        schedule_data = json.load(f)
                except:
                    schedule_data = []
                
                for idx, med in enumerate(schedule_data):
                    if scanned_med_name.lower() in med["name"].lower() or med["name"].lower() in scanned_med_name.lower():
                        if med.get("status") == "Pending":
                            match_found = True
                            schedule_data[idx]["status"] = "Taken"
                            with open(SCHEDULE_FILE, "w") as f:
                                json.dump(schedule_data, f, indent=4)
                            
                            st.success(f" Yes! Correct Medicine. In your Schedule **{med['name']}** is pending, Now 'Taken' marked!")
                            break
            
            if not match_found and scanned_med_name != "Unknown" and scanned_med_name != "Error reading API":
                st.error("❌ Wrong medicine, Not in schedule! Please cross-check.")

    st.markdown('</div>', unsafe_allow_html=True)

    # API configuration matrix badge loader status check
    status_color = "#02F70E" if api_keys else "#F10707"
    status_text  = f" Active ({len(api_keys)} Keys Configured)" if api_keys else " .env mein GEMINI_KEY_1 set karein"
    st.markdown(
        f"""
        <div class="section-card">
            <h3><i class="fa-solid fa-key"></i> API Status</h3>
            <p>Gemini Vision API: <b style="color:{status_color};">{status_text}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ── Emergency Alert Settings ─────────────────
def page_alerts():
    cura_logo("Emergency Alert Settings")
    alerts  = load_alerts()
    patient = load_patient()

    st.markdown('<div class="section-card"><h3><i class="fa-solid fa-bell"></i> Alert Configuration</h3>', unsafe_allow_html=True)

    with st.form("alerts_form"):
        col1, col2 = st.columns(2)
        with col1:
            whatsapp = st.text_input(
                "Family WhatsApp Number",
                value=alerts.get("whatsapp", patient.get("em_phone", "")),
                placeholder="+923001234567",
            )
            email = st.text_input(
                "Family Email",
                value=alerts.get("email", patient.get("em_email", "")),
                placeholder="family@gmail.com",
            )
        with col2:
            timeout = st.number_input(
                "Response Timeout (minutes)",
                value=int(alerts.get("timeout_minutes", 5)),
                min_value=1, max_value=30,
            )
            st.markdown("**Alert Tab**")
            whatsapp_on = st.checkbox("WhatsApp Alert On", value=alerts.get("whatsapp_on", True))
            email_on    = st.checkbox("Email Alert On",    value=alerts.get("email_on",    True))

        if st.form_submit_button(" Save Alert Settings ", use_container_width=True):
            save_json(ALERTS_FILE, {
                "whatsapp": whatsapp, "email": email,
                "timeout_minutes": timeout,
                "whatsapp_on": whatsapp_on, "email_on": email_on,
            })
            st.success(" Alert settings saved")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # How it works
    st.markdown(
        f"""
        <div class="section-card">
            <h3><i class="fa-solid fa-circle-info"></i> When did Aleart triggers?</h3>
            <p style="color:var(--text-secondary);">
                When patient not replyes Medicine Reminder for <b>{alerts.get('timeout_minutes', 5)} , CURA automatically:
            </p>
            <ul style="color:var(--text-secondary);line-height:2;">
                <li> Send WhatsApp message : <b>{alerts.get('whatsapp','—')}</b></li>
                <li> Sends Email: <b>{alerts.get('email','—')}</b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# DASHBOARD SIDEBAR
# ─────────────────────────────────────────────
def render_dashboard_sidebar():
    cura_sidebar_logo()

    # ── System status ──────────────────────────
    schedule = load_schedule()
    patient  = load_patient()
    pending  = sum(1 for m in schedule if m.get("status") == "Pending")
    missed   = sum(1 for m in schedule if m.get("status") == "Missed")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="padding:.5rem 0;">
            <div style="font-size:.7rem;text-transform:uppercase;opacity:.6;margin-bottom:.5rem;">System Status</div>
            <div style="font-size:.9rem;margin-bottom:.3rem;">
                <i class="fa-solid fa-circle" style="color:#4CAF50;font-size:.5rem;"></i>
                &nbsp; <b>CURA Active</b>
            </div>
            <div style="font-size:.85rem;opacity:.8;">
                 Patient: <b>{patient.get('name','Not set')}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Quick stats ────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="padding:.3rem 0;">
            <div style="font-size:.7rem;text-transform:uppercase;opacity:.6;margin-bottom:.6rem;">Quick Stats</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:.4rem;">
                <span style="opacity:.8;"> Total Medicines</span>
                <b>{len(schedule)}</b>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:.4rem;">
                <span style="opacity:.8;"> Pending</span>
                <b style="color:#FFB74D;">{pending}</b>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span style="opacity:.8;"> Missed</span>
                <b style="color:#EF9A9A;">{missed}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Navigation ─────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size:.7rem;text-transform:uppercase;opacity:.6;margin-bottom:.5rem;'>Navigation</div>",
        unsafe_allow_html=True,
    )

    pages = {
        "overview":  ("fa-gauge",        "Overview"),
        "patient":   ("fa-user-injured", "Patient Profile"),
        "schedule":  ("fa-pills",        "Medicine Schedule"),
        "companion": ("fa-microphone",   "chat Companion"),
        "camera":    ("fa-camera",       "Medicine Verify"),
        "alerts":    ("fa-bell",         "Emergency Alerts"),
    }

    current = st.session_state.get("page", "overview")
    for key, (icon, label) in pages.items():
        active = "active" if current == key else ""
        if st.sidebar.button(
            f"  {label}",
            key=f"nav_{key}",
            use_container_width=True,
        ):
            st.session_state["page"] = key
            st.rerun()

    # ── Logout + Danger zone ───────────────────
    st.sidebar.markdown("---")
    if st.sidebar.button(" Logout", key="sb_logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown(
        "<div style='font-size:.7rem;text-transform:uppercase;opacity:.6;margin:.8rem 0 .4rem;'>Danger Zone</div>",
        unsafe_allow_html=True,
    )
    if st.sidebar.button(" Delete Account", key="sb_delete", use_container_width=True):
        for path in (PROFILE_FILE, SCHEDULE_FILE, PATIENT_FILE, ALERTS_FILE):
            if os.path.exists(path):
                os.remove(path)
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown(
        "<small style='opacity:.5;font-size:.65rem;'>By deleting the acount all data will be removed and new user can be created.</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────
apply_cura_styles()
ensure_data_dir()

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "overview"

if st.session_state["auth"]:
    render_dashboard_sidebar()
    page = st.session_state.get("page", "overview")

    pages_map = {
        "overview":  page_overview,
        "patient":   page_patient,
        "schedule":  page_schedule,
        "companion": page_companion,
        "camera":    page_camera,
        "alerts":    page_alerts,
    }
    pages_map.get(page, page_overview)()
else:
    run_auth()