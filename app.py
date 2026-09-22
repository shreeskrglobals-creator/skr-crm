import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import json

# App Configuration
st.set_page_config(page_title="SKR Global CRM Pro", page_icon="🌍", layout="wide")

# Custom Title and Theme Styling
st.markdown("""
    <style>
    .main-title { font-size:2.4rem; font-weight:bold; color:#1E3A8A; margin-bottom:5px; }
    .subtitle { font-size:1.1rem; color:#4B5563; margin-bottom:20px; }
    .status-badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style>
""", unsafe_allowed_allowed=True)

st.markdown('<div class="main-title">🌍 Shree SKR Globals - Advanced Outreach & Lead CRM</div>', unsafe_allowed_html=True)
st.markdown('<div class="subtitle">Tailored for Nagpur, India (IST) | Real-time Country Peak Activity Tracker</div>', unsafe_allowed_html=True)

# 1. Precise Country Logistics (Waking up, Active on phone, Business Peak Window mapped to IST)
# Mapped specifically to target business responses based on your provided sheet
country_logistics = {
    "USA": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(18, 30),  # 6:30 PM IST (Their Morning Start)
        "peak_ist_end": time(2, 30),    # 2:30 AM IST (Their Afternoon Shift)
        "best_channel": "Email / WhatsApp",
        "status_now": "Checking early morning emails & waking up around 6:30 PM IST onwards."
    },
    "UK": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(13, 30),  # 1:30 PM IST
        "peak_ist_end": time(21, 30),   # 9:30 PM IST
        "best_channel": "Email / WhatsApp / Call",
        "status_now": "Highly active during Indian afternoon hours."
    },
    "Hong Kong": {
        "active_days": "Monday to Saturday",
        "peak_ist_start": time(6, 30),   # 6:30 AM IST
        "peak_ist_end": time(14, 30),  # 2:30 PM IST
        "best_channel": "WhatsApp / IM",
        "status_now": "Perfect morning window for Indian sellers."
    },
    "Japan": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(5, 30),   # 5:30 AM IST
        "peak_ist_end": time(13, 30),  # 1:30 PM IST
        "best_channel": "Email / Corporate Chat",
        "status_now": "Wakes up very early India time. High respect for quick responses."
    },
    "South Korea": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(5, 30),   # 5:30 AM IST
        "peak_ist_end": time(13, 30),  # 1:30 PM IST
        "best_channel": "IM / Email",
        "status_now": "Active early morning IST. Respond quickly to inquiries."
    },
    "Australia": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(4, 30),   # 4:30 AM IST
        "peak_ist_end": time(12, 30),  # 12:30 PM IST
        "best_channel": "WhatsApp / Call",
        "status_now": "Earliest market to follow up with. Ideal to message before noon IST."
    },
    "Thailand": {
        "active_days": "Monday to Saturday",
        "peak_ist_start": time(7, 30),   # 7:30 AM IST
        "peak_ist_end": time(15, 30),  # 3:30 PM IST
        "best_channel": "WhatsApp / IM",
        "status_now": "Highly active on instant messaging apps during mid-day."
    },
    "South Africa": {
        "active_days": "Monday to Friday",
        "peak_ist_start": time(12, 30),  # 12:30 PM IST
        "peak_ist_end": time(20, 30),  # 8:30 PM IST
        "best_channel": "Call / Email",
        "status_now": "Matches beautifully with Indian afternoon routines."
    }
}

# Real-time Nagpur Time Clock Engine
now_nd = datetime.now()
current_time_ist = now_nd.time()
current_day_str = now_nd.strftime("%A")

# 2. Native Dynamic Notification Engine (HTML5 Web Audio & Web Browser Alerts)
active_alerts = []
for country, data in country_logistics.items():
    is_active_day = True # General business day verification
    if "Saturday" not in data["active_days"] and current_day_str == "Saturday": is_active_day = False
    if current_day_str == "Sunday": is_active_day = False
    
    if is_active_day and (data["peak_ist_start"] <= current_time_ist <= data["peak_ist_end"]):
        active_alerts.append(f"🔔 ACTION REQUIRED: {country} clients are ACTIVE now! Channel: {data['best_channel']}. {data['status_now']}")

# Inject Alert Notification Banner on Screen & Sound Trigger
if active_alerts:
    st.toast("⚠️ Lead Windows Active! Check the system notification panel.", icon="🔔")
    # Play a light, harmless browser notification chime using simple HTML
    st.components.v1.html(
        """
        <audio autoplay style="display:none;">
            <source src="https://mixkit.co" type="audio/wav">
        </audio>
        <script>
        if (Notification.permission === "granted") {
            new Notification("SKR Globals Outreach Alert", {
                body: "Multiple target markets are awake and responsive right now! Open your dashboard to view action items.",
                icon: "https://flaticon.com"
            });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission();
        }
        </script>
        """,
        height=0
    )

# Sidebar - Live Nagpur Status Hub
st.sidebar.markdown(f"### ⏰ Live India Time (Nagpur)\n**{now_nd.strftime('%d-%b-%Y | %I:%M %p')}** ({current_day_str})")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔔 Active Real-Time Reminders")
if active_alerts:
    for alert in active_alerts:
        st.sidebar.warning(alert)
else:
    st.sidebar.success("✅ No urgent country windows active right now. Prepare next drafts!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Response Matrix Reference")
for c, d in country_logistics.items():
    st.sidebar.markdown(f"**{c}** ({d['active_days']}):\n`{d['peak_ist_start'].strftime('%I:%M %p')} - {d['peak_ist_end'].strftime('%I:%M %p')} IST`")

# Initialize Local CRM Data Storage
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        "Company Name", "Contact Person", "Country", "Lead Category", "Medicine Focus",
        "Preferred Channel", "What Customer Said", "Current Status", "Next Follow-up Date"
    ])

# Navigation Architecture
tab1, tab2, tab3 = st.tabs(["📊 Live CRM Matrix & Follow-ups", "➕ Add New Lead / Dropshipper", "💾 Secure Data Export"])

# Tab 2: Add New Lead / Dropshipper
with tab2:
    st.subheader("📥 Add a New Prospect / Supplier")
    with st.form("new_lead_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            comp_name = st.text_input("Company / Business Name *")
            contact_person = st.text_input("Contact Person Name")
            country_selected = st.selectbox("Target Country Location", list(country_logistics.keys()) + ["Other Location"])
            lead_cat = st.selectbox("Lead Category Type", ["Dropshipper", "Bulk Supplier", "Inquiry Reply", "Other"])
        with col2:
            med_focus = st.selectbox("Medicine Line Focus", ["Veterinary", "Phenergan", "Anti-Cancer", "All / General Portfolio", "None"])
            channel_pref = st.selectbox("Outreach Platform", ["WhatsApp", "Email", "IM / Direct Message", "Direct Call", "Save My Number Request"])
            lead_status = st.selectbox("Current Engagement Status", ["New / Uncontacted", "Introductory Message Sent", "Awaiting Reply ⏳", "Active Negotiation", "Follow-up Required", "Converted / Closed Deal 🏆"])
            next_follow = st.date_input("Scheduled Follow-up Action Date", datetime.today() + timedelta(days=2))
        
        cust_feedback = st.text_area("What did the customer say? / Exact response log history")
        
        submit_btn = st.form_submit_button("Lock Lead to App Memory")
        if submit_btn and comp_name:
            new_row = pd.DataFrame([{
                "Company Name": comp_name, "Contact Person": contact_person, "Country": country_selected,
                "Lead Category": lead_cat, "Medicine Focus": med_focus, "Preferred Channel": channel_pref,
                "What Customer Said": cust_feedback, "Current Status": lead_status, "Next Follow-up Date": next_follow.strftime('%Y-%m-%d')
            }])
            st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_row], ignore_index=True)
            st.success(f"✔️ Lead for '{comp_name}' saved into the active session database!")

# Tab 1: CRM & Live Action Dashboard
with tab1:
    st.subheader("💼 Active Sales Pipeline Management")
    df = st.session_state.leads_df
    
    if df.empty:
        st.info("Your SKR Globals CRM pipeline is empty. Go to the '+ Add New Lead' tab to populate your data sheet.")
    else:
        # Global Health Metrics Matrix
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Stored Leads", len(df))
        m2.metric("Pending Replies ⏳", len(df[df['Current Status'] == 'Awaiting Reply ⏳']))
        m3.metric("Follow-ups Due Today", len(df[df['Next Follow-up Date'] == datetime.today().strftime('%Y-%m-%d')]))
        m4.metric("Converted Clients 🏆", len(df[df['Current Status'] == 'Converted / Closed Deal 🏆']))
        
        st.markdown("---")
        
        # Action Alerts Section for Scheduled Followups
        today_str = datetime.today().strftime('%Y-%m-%d')
        due_today_df = df[df['Next Follow-up Date'] == today_str]
        if not due_today_df.empty:
            st.error(f"🚨 CRITICAL ACTION REQUIRED: You have {len(due_today_df)} follow-up touchpoints scheduled for today in India time! Review below:")
        
        # Editable Client Ledger Records
        st.markdown("### 📋 Interactive Customer Logs Ledger")
        for idx, row in df.iterrows():
            # Color code header status text visually
            header_title = f"🏢 {row['Company Name']} ({row['Country']}) — [{row['Lead Category']} | {row['Medicine Focus']}] — Status: {row['Current Status']}"
            if row['Next Follow-up Date'] == today_str:
