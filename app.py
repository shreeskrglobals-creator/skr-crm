import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# App Configuration
st.set_page_config(page_title="SKR Global CRM Pro", page_icon="🌍", layout="wide")

# Custom Title and Theme Styling (Fixed spelling parameter here)
st.markdown("""
    <style>
    .main-title { font-size:2.4rem; font-weight:bold; color:#1E3A8A; margin-bottom:5px; }
    .subtitle { font-size:1.1rem; color:#4B5563; margin-bottom:20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌍 Shree SKR Globals - Advanced Outreach & Lead CRM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tailored for Nagpur, India (IST) | Real-time Country Peak Activity Tracker</div>', unsafe_allowed_html=True)

# 1. Precise Country Logistics
country_logistics = {
    "USA": {"active_days": "Monday to Friday", "peak_ist_start": time(18, 30), "peak_ist_end": time(2, 30), "best_channel": "Email / WhatsApp", "status_now": "Checking early morning emails & waking up around 6:30 PM IST onwards."},
    "UK": {"active_days": "Monday to Friday", "peak_ist_start": time(13, 30), "peak_ist_end": time(21, 30), "best_channel": "Email / WhatsApp / Call", "status_now": "Highly active during Indian afternoon hours."},
    "Hong Kong": {"active_days": "Monday to Saturday", "peak_ist_start": time(6, 30), "peak_ist_end": time(14, 30), "best_channel": "WhatsApp / IM", "status_now": "Perfect morning window for Indian sellers."},
    "Japan": {"active_days": "Monday to Friday", "peak_ist_start": time(5, 30), "peak_ist_end": time(13, 30), "best_channel": "Email / Corporate Chat", "status_now": "Wakes up very early India time."},
    "South Korea": {"active_days": "Monday to Friday", "peak_ist_start": time(5, 30), "peak_ist_end": time(13, 30), "best_channel": "IM / Email", "status_now": "Active early morning IST."},
    "Australia": {"active_days": "Monday to Friday", "peak_ist_start": time(4, 30), "peak_ist_end": time(12, 30), "best_channel": "WhatsApp / Call", "status_now": "Earliest market to follow up with."},
    "Thailand": {"active_days": "Monday to Saturday", "peak_ist_start": time(7, 30), "peak_ist_end": time(15, 30), "best_channel": "WhatsApp / IM", "status_now": "Highly active on instant messaging apps during mid-day."},
    "South Africa": {"active_days": "Monday to Friday", "peak_ist_start": time(12, 30), "peak_ist_end": time(20, 30), "best_channel": "Call / Email", "status_now": "Matches beautifully with Indian afternoon routines."}
}

# Real-time Nagpur Time Clock Engine
now_nd = datetime.now()
current_time_ist = now_nd.time()
current_day_str = now_nd.strftime("%A")

# 2. Native Dynamic Notification Engine
active_alerts = []
for country, data in country_logistics.items():
    is_active_day = True 
    if "Saturday" not in data["active_days"] and current_day_str == "Saturday": is_active_day = False
    if current_day_str == "Sunday": is_active_day = False
    
    if data["peak_ist_start"] <= data["peak_ist_end"]:
        is_active_time = data["peak_ist_start"] <= current_time_ist <= data["peak_ist_end"]
    else:
        is_active_time = current_time_ist >= data["peak_ist_start"] or current_time_ist <= data["peak_ist_end"]

    if is_active_day and is_active_time:
        active_alerts.append(f"🔔 {country} clients are ACTIVE now! ({data['best_channel']})")

if active_alerts:
    st.toast("⚠️ Active Lead Windows Open!", icon="🔔")

# Sidebar UI
st.sidebar.markdown(f"### ⏰ Live India Time (Nagpur)\n**{now_nd.strftime('%d-%b-%Y | %I:%M %p')}** ({current_day_str})")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔔 Active Real-Time Reminders")
if active_alerts:
    for alert in active_alerts: st.sidebar.warning(alert)
else:
    st.sidebar.success("✅ No urgent country windows active right now.")

# Initialize Storage
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        "Company Name", "Contact Person", "Country", "Lead Category", "Medicine Focus",
        "Preferred Channel", "What Customer Said", "Current Status", "Next Follow-up Date"
    ])

# Daily File Upload Engine
st.markdown("### 📥 Import Daily Business File")
uploaded_file = st.file_uploader("Upload your saved CSV file to resume tracking", type=["csv"])

if uploaded_file is not None and ('file_loaded' not in st.session_state or st.session_state.file_loaded != uploaded_file.name):
    try:
        loaded_df = pd.read_csv(uploaded_file)
        required_cols = ["Company Name", "Contact Person", "Country", "Lead Category", "Medicine Focus", "Preferred Channel", "What Customer Said", "Current Status", "Next Follow-up Date"]
        for col in required_cols:
            if col not in loaded_df.columns:
                loaded_df[col] = ""
        st.session_state.leads_df = loaded_df[required_cols]
        st.session_state.file_loaded = uploaded_file.name
        st.success(f"📈 Loaded {len(loaded_df)} leads from {uploaded_file.name} successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Navigation
tab1, tab2, tab3 = st.tabs(["📊 Live CRM Matrix & Follow-ups", "➕ Add New Lead / Dropshipper", "💾 Secure Data Export"])

# Tab 2: Add New Lead
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
            st.success(f"✔️ Lead for '{comp_name}' saved!")
            st.rerun()

# Tab 1: Dashboard View
with tab1:
    st.subheader("💼 Active Sales Pipeline Management")
    df = st.session_state.leads_df
    today_str = datetime.today().strftime('%Y-%m-%d')
    
    if df.empty:
        st.info("Your pipeline is currently empty. Upload your CSV file above or add a new lead to get started.")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Stored Leads", len(df))
        m2.metric("Pending Replies ⏳", len(df[df['Current Status'] == 'Awaiting Reply ⏳']))
        m3.metric("Follow-ups Due Today", len(df[df['Next Follow-up Date'] == today_str]))
        m4.metric("Converted Clients 🏆", len(df[df['Current Status'] == 'Converted / Closed Deal 🏆']))
        
        st.markdown("---")
        
        st.markdown("### 📋 Interactive Customer Logs Ledger")
        for idx, row in df.iterrows():
            is_due = (str(row['Next Follow-up Date']) == today_str)
            label_prefix = "🚨 [DUE TODAY] " if is_due else "🏢 "
            header_title = f"{label_prefix}{row['Company Name']} ({row['Country']}) — Status: {row['Current Status']}"
                
            with st.expander(header_title):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"👤 **Primary Contact:** {row['Contact Person']}")
                    st.markdown(f"📱 **Outreach via:** `{row['Preferred Channel']}`")
                    st.markdown(f"💊 **Product Segment:** `{row['Medicine Focus']}`")
                    st.info(f"💬 **Last Notes:** {row['What Customer Said']}")
                with col_b:
                    status_list = ["New / Uncontacted", "Introductory Message Sent", "Awaiting Reply ⏳", "Active Negotiation", "Follow-up Required", "Converted / Closed Deal 🏆"]
                    status_idx = status_list.index(row['Current Status']) if row['Current Status'] in status_list else 0
                    updated_status = st.selectbox("Modify Status", status_list, key=f"status_mod_{idx}", index=status_idx)
                    
                    try:
                        parsed_date = datetime.strptime(str(row['Next Follow-up Date']), '%Y-%m-%d')
                    except:
                        parsed_date = datetime.today()
                    updated_date = st.date_input("Reschedule Date", parsed_date, key=f"date_mod_{idx}")
                
                updated_feed = st.text_area("Log Fresh Response Text Here:", value=str(row['What Customer Said']), key=f"feed_mod_{idx}")
                
                if st.button("Update Entry", key=f"save_mod_btn_{idx}"):
                    st.session_state.leads_df.at[idx, 'Current Status'] = updated_status