import streamlit as st
import os
import json
from google.oauth2.credentials import Credentials
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import build_resource_service

st.set_page_config(page_title="Personal Email Agent", page_icon="📧")
st.title("סוכן האימייל האישי שלי")

# משיכת מפתח ג'מיני מהסודות של סטרימליט
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("חסר מפתח API של ג'מיני בהגדרות הסודות.")
    st.stop()

def initialize_gmail_agent():
    # משיכת פרטי הגישה לג'ימייל מהסודות של סטרימליט
    try:
        creds_data = {
            "token": st.secrets["GMAIL_TOKEN"],
            "refresh_token": st.secrets["GMAIL_REFRESH_TOKEN"],
            "token_uri": st.secrets["GMAIL_TOKEN_URI"],
            "client_id": st.secrets["GMAIL_CLIENT_ID"],
            "client_secret": st.secrets["GMAIL_CLIENT_SECRET"],
            "scopes": ["https://www.googleapis.com/auth/gmail.modify"]
        }
        credentials = Credentials.from_authorized_user_info(creds_data)
        api_resource = build_resource_service(credentials=credentials)
        toolkit = GmailToolkit(api_resource=api_resource)
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        
        agent = initialize_agent(
            tools=toolkit.get_tools(),
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        return agent
    except Exception as e:
        st.error(f"שגיאה בהתחברות ל-Gmail: {e}")
        return None

if "agent" not in st.session_state:
    with st.spinner("מתחבר ל-Gmail..."):
        st.session_state.agent = initialize_gmail_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("מה תרצה שהסוכן יעשה?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.agent:
        with st.chat_message("assistant"):
            with st.spinner("חושב ומבצע..."):
                response = st.session_state.agent.run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
