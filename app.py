import streamlit as st
import google.generativeai as genai
import os
 
# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Leaders Life Line", page_icon="🛡️", layout="wide")
 
# --- API CONFIGURATION ---
# In production, this pulls securely from Streamlit's secrets manager so it isn't public.
API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')
 
# --- CRISIS INTERCEPT FUNCTION ---
def check_crisis(text):
    crisis_keywords = ['suicide', 'kill myself', 'end it', 'no way out', 'want to die']
    if any(word in text.lower() for word in crisis_keywords):
        return True
    return False
 
# --- UI: SIDEBAR PROFILE SELECTOR ---
st.sidebar.title("👤 Contextual Profile")
st.sidebar.markdown("Select parameters to filter doctrine and resources appropriately.")
 
component = st.sidebar.selectbox("Service Component", ["Army", "Navy", "Air Force", "Marines", "Coast Guard", "Space Force"])
status = st.sidebar.selectbox("Duty Status", ["Active Duty", "National Guard", "Reserve", "Veteran"])
rank = st.sidebar.selectbox("Rank Structure", ["Officer", "Warrant Officer", "Enlisted"])
 
st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **Security Notice:** Do not enter PII or PHI (Names, SSNs, specific unit designations). Session data is not saved.")
 
# --- UI: MAIN INTERFACE ---
st.title("🛡️ Leaders Life Line")
st.markdown("**Root Cause Analysis & Outcome Possibility Matrix**")
st.write("Input the circumstances or struggles the service member is facing. The AI will analyze doctrine and provide resource mapping, COAs, and pre-counseling guidance.")
 
# Text Input
user_input = st.text_area("Describe the Circumstances:", height=200, placeholder="e.g., I have a TPU reservist who just failed their second ACFT and is struggling financially...")
 
if st.button("Analyze Circumstance & Find Resources"):
    if user_input:
        # 1. Check for Crisis
        if check_crisis(user_input):
            st.error("🚨 **CRISIS ALERT: If you or a service member are in immediate danger, dial 988 and press 1 for the Veterans Crisis Line.**")
            st.write("Alternatively, text 838255 or visit [VeteransCrisisLine.net](https://www.veteranscrisisline.net/).")
            st.stop() # Stops the rest of the code from running
       
        with st.spinner("Analyzing doctrine and mapping resources..."):
           
            # 2. Construct the RAG Prompt
            # (In phase 2, this is where we inject the database documents. For now, we use the LLM's baseline knowledge).
            system_prompt = f"""
            You are 'Leaders Life Line', an expert military staff officer and empathetic mentor.
            Analyze the following circumstance for a {component} {status} {rank}.
           
            Provide a structured response using markdown with the following sections:
            1. **Root Cause Analysis:** Identify primary and secondary stressors.
            2. **Administrative Reality (Outcome Matrix):** What are the real regulatory consequences (e.g., chapters, retention)? Do not sugarcoat, provide factual doctrine.
            3. **Resource Mapping:** List specific, actionable resources based on the 7 pillars (Command, Community, VA, etc.) relevant to a {status} {component} {rank}.
            4. **Pre-Counseling Prep:** Provide 3 empathetic talking points for the leader to use when discussing this with the service member.
           
            Circumstance: {user_input}
            """
          
            # 3. Call the AI
            try:
                response = model.generate_content(system_prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error("An error occurred while connecting to the AI. Please check your API key.")

    else:

        st.warning("Please enter a circumstance to analyze.")
