import streamlit as st
from google import genai
import os
 
# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Leaders Life Line", page_icon="🛡️", layout="wide")
 
# --- SECURE API RETRIEVAL ---
# This version checks multiple ways to find your key
API_KEY = st.secrets.get("GEMINI_API_KEY")
 
# --- UI: MAIN INTERFACE ---
st.title("🛡️ Leaders Life Line")
 
if not API_KEY:
    st.error("🛑 **System Error: API Key Not Found.**")
    st.info("""
    **To fix this:**
    1. Go to your Streamlit Cloud Dashboard.
    2. Click 'Settings' -> 'Secrets' for this app.
    3. Ensure you have entered exactly: 
       `GEMINI_API_KEY = "your-key-here"`
    """)
    st.stop()
 
# Initialize Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize AI Client: {e}")
    st.stop()
 
# --- CRISIS INTERCEPT ---
def check_crisis(text):
    crisis_keywords = ['suicide', 'kill myself', 'end it', 'no way out', 'want to die']
    if any(word in text.lower() for word in crisis_keywords):
        return True
    return False
 
# --- SIDEBAR ---
st.sidebar.title("👤 Contextual Profile")
component = st.sidebar.selectbox("Service Component", ["Army", "Navy", "Air Force", "Marines", "Coast Guard", "Space Force"])
status = st.sidebar.selectbox("Duty Status", ["Active Duty", "National Guard", "Reserve", "Veteran"])
rank = st.sidebar.selectbox("Rank Structure", ["Officer", "Warrant Officer", "Enlisted"])

st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **Security Notice:** Do not enter PII or PHI (Names, SSNs, specific unit designations). Session data is not saved.")

# --- INPUT ---
user_input = st.text_area("Describe the Circumstances:", height=200)
 
if st.button("Analyze Circumstance"):
    if user_input:
        if check_crisis(user_input):
            st.error("🚨 **CRISIS ALERT: Dial 988 and press 1 for the Veterans Crisis Line.**")
            st.stop()
       
        with st.spinner("Analyzing..."):
            try:
                # Use the 'flash' model for speed and reliability
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=f"Context: {component} {status} {rank}. Analyze: {user_input}"
                )
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                # This will print the EXACT error from Google (e.g. 403 Forbidden)
                st.error(f"Google AI Error: {e}")
    else:
        st.warning("Please enter details first.")
