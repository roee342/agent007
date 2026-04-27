import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="Agent JB", page_icon="🤖")
st.title("JB")

# 2. Safe Library Check (Prevents the app from breaking during setup)
try:
    from langchain.agents import initialize_agent, AgentType
    from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
    libraries_loaded = True
except ImportError as e:
    libraries_loaded = False
    st.error(f"Setup in progress: Still installing background libraries... ({e})")
    st.info("Please go to 'Manage app' -> '⋮' -> 'Reboot app' in Streamlit.")

# 3. Check for API Keys
gemini_key = st.secrets.get("GEMINI_API_KEY")
gmail_token = st.secrets.get("GMAIL_TOKEN")

if not gemini_key and libraries_loaded:
    st.warning("⚠️ Setup incomplete: Please add your API keys in Streamlit Secrets to activate the agent.")

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi Roee! I'm your personal email agent. How can I help you today?"}
    ]

# 5. Render Existing Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input & Chat Logic
if prompt := st.chat_input("Type your message here..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show assistant response
    with st.chat_message("assistant"):
        if not libraries_loaded:
            response = "I can't respond yet. Waiting for libraries to install."
            st.error(response)
        elif not gemini_key:
            response = "I'm currently offline. Please configure my API keys in Streamlit Secrets."
            st.error(response)
        else:
            # Placeholder for the actual Agent logic
            response = f"I received your request: '{prompt}'. (Full Gmail logic will run here once keys are set!)"
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
