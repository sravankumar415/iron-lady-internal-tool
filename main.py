import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Iron Lady Admin", layout="wide")

# This safely gets your API key from Streamlit's Secret settings
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🛡️ Iron Lady: Internal Lead Manager")

if 'leads' not in st.session_state:
    st.session_state.leads = pd.DataFrame([
        {"Name": "Anjali Gupta", "Type": "Professional", "Status": "Interested"}
    ])

# --- CREATE ---
with st.sidebar:
    st.header("Add New Lead")
    name = st.text_input("Name")
    l_type = st.selectbox("Type", ["Professional", "Entrepreneur", "Restarter"])
    if st.button("Save Lead"):
        new_row = {"Name": name, "Type": l_type, "Status": "New"}
        st.session_state.leads = pd.concat([st.session_state.leads, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Lead Added!")

# --- READ, UPDATE, DELETE ---
st.write("### Current Lead Table")
updated_df = st.data_editor(st.session_state.leads, num_rows="dynamic")
st.session_state.leads = updated_df

# --- AI FEATURE ---
st.divider()
st.header("🤖 AI Outreach Generator")
if not st.session_state.leads.empty:
    target = st.selectbox("Select a lead to message:", st.session_state.leads['Name'])
    if st.button("Generate Strategy Email"):
        prompt = f"Write a short, powerful email to {target} who is an {l_type}. Mention the Iron Lady Business Warfare program."
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        st.info(response.choices[0].message.content)
