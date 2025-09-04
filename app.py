# --------------------------------------------------------------------------
# SpeakQL : Main app file
# To run: streamlit run app.py
# --------------------------------------------------------------------------

# Main imports
import streamlit as st
import os
import time
import speech_recognition as sr
import wave
import io
import pyperclip


# For dev env ------------------------------------------------------------
# from dotenv import load_dotenv
# from eralchemy import render_er
# Load environment variables
# load_dotenv()



# def save_api_keys(langchain_key, model_key, selected_model):
#     """Save API keys to environment variables."""
#     if langchain_key:
#         os.environ["LANGSMITH_API_KEY"] = langchain_key
#         st.session_state["langsmith_key_set"] = True
    
#     if model_key:
#         if selected_model == "Groq":
#             os.environ["GROQ_API_KEY"] = model_key
#             st.session_state["model_key_set"] = True
#         elif selected_model == "OpenAI":
#             os.environ["OPENAI_API_KEY"] = model_key
#             st.session_state["model_key_set"] = True
#         elif selected_model == "Anthropic":
#             os.environ["ANTHROPIC_API_KEY"] = model_key
#             st.session_state["model_key_set"] = True
# --------------------------------------------------------------------------

# ----------------------- ER Diagram box -----------------------------------
@st.dialog("ER Diagram", width="large")
def generate_er(img_path, db_url):
    st.write("This is the ER Diagram")
    st.image(img_path, caption=db_url)
    if st.button("Okay"):
        st.rerun()

# ----------------------- API Keys box -----------------------------------
@st.dialog("API Keys")
def api_keys_box(curr_model):
    l_api_key = st.text_input("Enter LangSmith API Key", type="password", key='langsmith')
    m_api_key = st.text_input(f"Enter {curr_model} API Key", type="password", key='model_api_key')
    
    if st.button("Submit"):
        st.toast("API Keys saved successfully!")
        st.rerun()

if 'welcome' not in st.session_state:
        st.session_state.welcome = True

# ----------------------- Welcome Message box -----------------------------------
@st.dialog("Welcome to SpeakQL")
def welcome_box():
    st.write("Directly speak to your database. No SQL queries needed! Ask your questions in chat or use voice input. View ER diagram for reference.")
    st.write("This demo is powered by **gpt-4o-mini** and the **Chinook** database.")
    st.markdown("### Explore:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔹 SpeakQL")
        st.success("⚡ Runs instantly with basic logic.")
        st.caption("Ask simple questions like:")
        st.caption("- How many customers are there?")
        st.caption("- What are the names of different artists?")
        
    with col2:
        st.subheader("🔸 SpeakQL Pro")
        st.info("🧠 Ideal for complex questions. Uses AI agents.")
        st.caption("- What’s the total revenue per genre?")
        st.caption("- Which artist had the most album sales in 2009?")
    
    st.markdown(" 🏢 Want to Learn More? Visit **SpeakQL for Enterprise** ")
    st.caption("⚠️ This app may produce incorrect results. Always verify critical data.")
    

    st.session_state.welcome = False
        

# ----------------------- Main function -----------------------------------
def main():
    # Page configuration
    st.set_page_config(
        page_title="SpeakQL",
        page_icon="🗣️",
        layout="wide"
    )
    if st.session_state.welcome:
        welcome_box()

    # Initialize session state for API key
    if "langsmith_key_set" not in st.session_state:
        st.session_state["langsmith_key_set"] = False
    if "model_key_set" not in st.session_state:
        st.session_state["model_key_set"] = False

    # 3 App pages -> Home, Pro, Enterprise (About Section)
    pages = {
        "": [
            st.Page("utils/home_page.py", title="SpeakQL"),
            st.Page("utils/sql_agent.py", title="SpeakQL Pro"),
            st.Page("utils/enterprise.py", title="SpeakQL for Enterprise"),
        ]
    }

    # Database connection box ------------------------------------------------
    if 'db_conn_status' not in st.session_state:
        st.session_state.db_conn_status = "Database Connected"

    if 'db_uri' not in st.session_state:
        st.session_state.db_uri = 'sqlite:///data/Chinook.db'
    
    if 'db_icon' not in st.session_state:
        st.session_state.db_icon = 'database' #database_off to turn off
    
    if 'human_in_the_loop' not in st.session_state:
        st.session_state.human_in_the_loop = False

    with st.sidebar.expander(st.session_state.db_conn_status, icon=f":material/{st.session_state.db_icon}:"):
        st.write("Add database details")
        db_url = st.text_input("Database URI ", key='db_url', value=st.session_state.db_uri)

        if st.button("Connect", key='db_conn_btn', type='primary', disabled=True):
            st.session_state.db_conn_status = "Database Connected"
            st.session_state.db_icon = 'database'
            st.rerun()
    # --------------------------------------------------------------------------
    
    
    # ER Diagram box ------------------------------------------------------------
    img_name = 'chinhook_arch.png'
    output_path = os.path.join(os.getcwd(), 'data', img_name)
    # render_er(db_url, output_path) ---> will render while setup.
    if st.sidebar.button("ER Diagram", use_container_width=True, type='primary'):
        generate_er(output_path, db_url)

    # Model selection box ------------------------------------------------
    #st.session_state.human_in_the_loop = st.sidebar.toggle("Human in the loop")
    curr_model = st.sidebar.selectbox("Select Model", ["OpenAI", "Grok", "Llama"], key="model") 

    if st.sidebar.button("API Keys", icon=':material/key_vertical:', use_container_width=True):
        api_keys_box(curr_model)

    
        
    # ----------------------- Voice input  -----------------------------------
    audio = st.sidebar.audio_input("Try Voice Input")
    if audio:
        #st.warning("Unfortunately, audio translation is not working.")
        r = sr.Recognizer()
        audio_bytes = audio.getvalue()
        with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
            sample_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            raw_data = wf.readframes(wf.getnframes())
        audio_data = sr.AudioData(raw_data, sample_rate, sample_width)
        with st.sidebar.empty():
            try:
                with st.spinner("Please wait...", show_time=True):
                    text = r.recognize_google(audio_data)
                    text = text.lower()
                st.info(f"{text}  (Please paste in Chat)")
                #pyperclip.copy(text) --->  copy issue in prod
            except sr.UnknownValueError:
                st.warning("Could not understand audio.")
            except sr.RequestError as e:
                st.error(f"Speech recognition failed: {e}")
    # if st.sidebar.button("Try Voice", icon=':material/mic:', type="secondary", use_container_width=True):
    #     voice.speech_to_text()

    # ----------------------- Voice end -----------------------------------

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main() 