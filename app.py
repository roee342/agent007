import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="Agent JB", page_icon="🤖")
st.title("JB")

# 2. Check for API Keys in Secrets (ללא ספריות חיצוניות שמפילות את הקוד)
gemini_key = st.secrets.get("GEMINI_API_KEY")
gmail_token = st.secrets.get("GMAIL_TOKEN")

if not gemini_key or not gmail_token:
    st.warning("⚠️ Setup incomplete: Please add your API keys in Streamlit Secrets (Manage App -> Settings -> Secrets).")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi Roee! The interface is fully working. Once you add the API keys, we can connect my brain."}
    ]

# 4. Render Existing Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Chat Logic
if prompt := st.chat_input("Type your message here..."):
    # הצגת הודעת המשתמש
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # תגובת הסוכן
    with st.chat_message("assistant"):
        if not gemini_key:
            response = "I'm currently offline. I need my Gemini API Key to think."
            st.error(response)
        else:
            response = f"I received: '{prompt}'. (LangChain logic will be connected here!)"
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
