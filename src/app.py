import streamlit as st
from dotenv import load_dotenv
import os
import time
# Load environment variables
load_dotenv()

def save_api_keys(langchain_key, model_key, selected_model):
    """Save API keys to environment variables."""
    if langchain_key:
        os.environ["LANGSMITH_API_KEY"] = langchain_key
        st.session_state["langsmith_key_set"] = True
    
    if model_key:
        if selected_model == "Groq":
            os.environ["GROQ_API_KEY"] = model_key
            st.session_state["model_key_set"] = True
        elif selected_model == "OpenAI":
            os.environ["OPENAI_API_KEY"] = model_key
            st.session_state["model_key_set"] = True
        elif selected_model == "Anthropic":
            os.environ["ANTHROPIC_API_KEY"] = model_key
            st.session_state["model_key_set"] = True


    
def page_2():
    st.title("Page 2")
    st.write("This is page 2")

def main():
    st.set_page_config(
        page_title="SpeakQL",
        page_icon="🚀",
        layout="wide"
    )
    
    # Initialize session state for API key status
    if "langsmith_key_set" not in st.session_state:
        st.session_state["langsmith_key_set"] = False
    if "model_key_set" not in st.session_state:
        st.session_state["model_key_set"] = False


    pages = {
        "Your account": [
            st.Page("home_page.py", title="Home"),
            st.Page(page_2, title="Manage your account"),
        ]
    }

    st.sidebar.text_input("Database URI ", key='side_db_uri', value='sqlite:///Chinook.db')
    curr_model = st.sidebar.selectbox("Select Model", ["Llama", "OpenAI", "Groq"], key="model")
    # with st.sidebar.expander("API Keys"):
    #     st.text_input("Enter LangSmith API Key", type="password")
    #     st.text_input(f"Enter {curr_model} API Key", type="password")

    @st.dialog("API Keys")
    def vote(curr_model):
        os.environ["LANGSMITH_API_KEY"] = st.text_input("Enter LangSmith API Key", type="password", key='langsmith')
        os.environ[f"{curr_model.upper()}_API_KEY"] = st.text_input(f"Enter {curr_model} API Key", type="password", key='model_api_key')
        if st.button("Submit"):
            st.toast("API Keys saved successfully!")
            st.rerun()

    if st.sidebar.button("API Keys", use_container_width=True, type='primary'):
        vote(curr_model)
        
        

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main() 