import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# App Configuration
st.set_page_config(page_title="SKR Global CRM", page_icon="🌍", layout="wide")
st.title("🌍 Shree SKR Globals - Lead & Outreach Manager")

# 1. Timezone Setup (Targeting Peak Local Hours 9 AM - 5 PM converted to IST)
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
st.sidebar.markdown(f"### ⏰ Current India Time (IST)\n**{now_ist.strftime('%d-%b-%Y %I:%M %p')}**")

country_windows = {
    "USA (EST)": {"window": "6:30 PM to 2:30 AM IST", "hint": "Best for night outreach"},
    "UK (GMT)": {"window": "1:30 PM to 9:30 PM IST", "hint": "Best for afternoon outreach"},
    "UAE (GST)": {"window": "10:30 AM to 6:30 PM IST", "hint": "Perfect daytime overlap"},
    "Australia (AEST)": {"window": "4:30 AM to 12:30 PM IST", "hint": "Best for early morning outreach"}
}

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Best Response Windows (IST)")
for country, data in country_windows.items():
    st.sidebar.markdown(f"**{country}**:\n`{data['window']}`\n*{data['hint']}*")

# 2. Initialize Data Store
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = pd.DataFrame(columns=[
        "Company Name", "Contact Person", "Country", "Channel", 
        "Customer Feedback / Notes", "Status", "Next Follow-up Date"
    ])

# Tabs for Navigation
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Follow-ups", "➕ Add New Lead", "💾 Export & Backup"])

with tab2:
    st.subheader("Add a New Client Lead")
    with st.form("lead_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            comp = st.text_input("Company Name")
            contact = st.text_input("Contact Person Name")
            country = st.selectbox("Target Country", list(country_windows.keys()) + ["Other"])
        with col2:
            channel = st.selectbox("Preferred Channel", ["WhatsApp", "Email", "Call", "LinkedIn"])
            status = st.selectbox("Initial Status", ["New / No Contact", "Awaiting Reply", "Active Negotiation", "Converted"])
            follow_date = st.date_input("Next Follow-up Date", datetime.today() + timedelta(days=3))
        
        feedback = st.text_area("What did the customer say? / Initial Notes")
        submitted = st.form_submit_button("Save Lead to CRM")
        
        if submitted and comp:
            new_row = pd.DataFrame([{
                "Company Name": comp, "Contact Person": contact, "Country": country, 
                "Channel": channel, "Customer Feedback / Notes": feedback, 
                "Status": status, "Next Follow-up Date": follow_date.strftime('%Y-%m-%d')
            }])
            st.session_state.leads_df = pd.concat([st.session_state.leads_df, new_row], ignore_index=True)
            st.success(f"🎉 Lead '{comp}' successfully saved!")

with tab1:
    st.subheader("Your Lead Matrix")
    df = st.session_state.leads_df
    
    if df.empty:
        st.info("Your pipeline is currently empty. Head over to the '+ Add New Lead' tab to input your business data.")
    else:
        # Mini KPIs
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Active Leads", len(df))
        c2.metric("Awaiting Reply ⏳", len(df[df['Status'] == 'Awaiting Reply']))
        c3.metric("Converted Clients 🏆", len(df[df['Status'] == 'Converted']))
        
        st.markdown("---")
        
        # Interactive Grid Updates
        for idx, row in df.iterrows():
            with st.expander(f"💼 {row['Company Name']} ({row['Country']}) — Status: {row['Status']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"👤 **Contact:** {row['Contact Person']} | 📱 **Via:** {row['Channel']}")
                    st.write(f"📅 **Next Follow-up Date:** `{row['Next Follow-up Date']}`")
                with col_b:
                    new_status = st.selectbox("Update Status", ["New / No Contact", "Awaiting Reply", "Active Negotiation", "Converted"], key=f"status_{idx}", index=["New / No Contact", "Awaiting Reply", "Active Negotiation", "Converted"].index(row['Status']))
                    new_date = st.date_input("Change Follow-up Date", datetime.strptime(row['Next Follow-up Date'], '%Y-%m-%d'), key=f"date_{idx}")
                
                new_feed = st.text_area("Update What Customer Said:", value=row['Customer Feedback / Notes'], key=f"feed_{idx}")
                
                if st.button("Save Updates for this Client", key=f"btn_{idx}"):
                    st.session_state.leads_df.at[idx, 'Status'] = new_status
                    st.session_state.leads_df.at[idx, 'Next Follow-up Date'] = new_date.strftime('%Y-%m-%d')
                    st.session_state.leads_df.at[idx, 'Customer Feedback / Notes'] = new_feed
                    st.rerun()

with tab3:
    st.subheader("Backup Your Business Data")
    st.write("Download your complete lead history into an Excel-friendly CSV spreadsheet anytime.")
    if not st.session_state.leads_df.empty:
        csv_data = st.session_state.leads_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Sheet (.csv)",
            data=csv_data,
            file_name=f"SKR_Globals_Leads_{datetime.today().strftime('%Y-%m-%d')}.csv",
            mime='text/csv'
        )
    else:
        st.warning("No data available yet to export.")
