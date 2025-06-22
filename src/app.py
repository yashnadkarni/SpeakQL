import streamlit as st
from dotenv import load_dotenv
import os
import time
from eralchemy import render_er
import voice
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


@st.dialog("ER Diagram", width="large")
def generate_er(img_path, db_url):
    st.write("This is the ER Diagram")
    st.image(img_path, caption=db_url)
    if st.button("Okay"):
        st.rerun()

@st.dialog("API Keys")
def vote(curr_model):
    os.environ["LANGSMITH_API_KEY"] = st.text_input("Enter LangSmith API Key", type="password", key='langsmith')
    os.environ[f"{curr_model.upper()}_API_KEY"] = st.text_input(f"Enter {curr_model} API Key", type="password", key='model_api_key')
    if st.button("Submit"):
        st.toast("API Keys saved successfully!")
        st.rerun()

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
            st.Page("home_page.py", title="SpeakQL"),
            st.Page("sql_agent.py", title="SpeakQL Pro"),
            st.Page("enterprise.py", title="SpeakQL for Enterprise"),
        ]
    }

    db_url = st.sidebar.text_input("Database URI ", key='side_db_uri', value='sqlite:///Chinook.db')
    st.sidebar.write("Enlarge for fullscreen")
    img_name = 'chinhook_arch.png'
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_dir, 'data', img_name)
    render_er(db_url, output_path)
    st.sidebar.image(output_path)
    if st.sidebar.button("Generate ER Diagram", use_container_width=True, type='primary'):
        generate_er(output_path, db_url)


    curr_model = st.sidebar.selectbox("Select Model", ["Llama", "OpenAI", "Groq"], key="model") 

    if st.sidebar.button("API Keys", icon=':material/key_vertical:', use_container_width=True):
        vote(curr_model)

    if st.sidebar.button("Try Voice", icon=':material/mic:', type="secondary", use_container_width=True):
        voice.speech_to_text()
        
        

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main() 