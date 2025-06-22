# import os
# from eralchemy import render_er
# ## Draw from database
# db_url = "sqlite:///Chinook.db"
# root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# output_path = os.path.join(root_dir, 'data', 'chinhook_arch.png')

# render_er(db_url, output_path)

# Text to speech


# Python program to translate
# speech to text and text to speech  ****************** WORKS!!!!!!! ******************


# import speech_recognition as sr
# import pyttsx3 

# import streamlit as st



# st.set_page_config(
#         page_title="Sandbox",
#         page_icon="🧪",
#         layout="wide"
#     )


# # Initialize the recognizer 
# r = sr.Recognizer() 

# # Function to convert text to
# # speech
# def SpeakText(command):
    
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command) 
#     engine.runAndWait()
    
    
# Loop infinitely for user to
# speak

# st.title(" Just checking speech to text !!!!")

# if "prompt_placeholder" not in st.session_state:
#     st.session_state.prompt_placeholder = "Enter your question"

# audio, text = st.columns([0.1, 0.9])
# with audio:
#     audio_value = st.audio_input("Record a voice message")
    
#     if audio_value:
#         st.write(audio_value)
#         MyText = r.recognize_google(audio_value)
#         MyText = MyText.lower()
#         st.write(f"Did you say: {MyText}")
#         st.session_state.prompt_placeholder = MyText

# with text:
#     prompt = st.chat_input(st.session_state.prompt_placeholder)



# Exception handling to handle
# exceptions at the runtime
# MyText = ""
# with audio:
#     if st.button("", icon=":material/mic:", type="tertiary"):  ##     Use st.pill()
#         try:
#             with sr.Microphone() as source2:
#                 r.adjust_for_ambient_noise(source2, duration=0.2)
#                 audio2 = r.listen(source2)
#                 MyText = r.recognize_google(audio2)
#                 MyText = MyText.lower()
#                 st.session_state.prompt_placeholder = MyText
#                 print("Did you say" ,MyText)
#                 #SpeakText(MyText)
            
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))

#         except sr.UnknownValueError:
#             print("unknown error occurred")
        

# with text:
#     prompt = st.chat_input(st.session_state.prompt_placeholder)

# st.write(f"Did you say: {MyText}")

# 8****************************************************************************************************
# while(1):    
    
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
        
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
            
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level 
#             r.adjust_for_ambient_noise(source2, duration=0.2)
            
#             #listens for the user's input 
#             audio2 = r.listen(source2)
            
#             # Using google to recognize audio
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()

#             print("Did you say" ,MyText)
#             SpeakText(MyText)
            
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
        
#     except sr.UnknownValueError:
#         print("unknown error occurred")

#_________________________________ ChatGPT _________________________________________
import streamlit as st
import speech_recognition as sr
import wave
import io
import pyperclip


st.set_page_config(page_title="Voice Chat", page_icon="🎤", layout="wide")

r = sr.Recognizer()

if "prompt_placeholder" not in st.session_state:
    st.session_state.prompt_placeholder = "Ask something..."

st.title("🎤 Voice to Chat Interface")

#----------------------------- Dialog box  ----------------------------------------------------------------
@st.dialog("Voice Input")
def speech_to_text():
    if "user_speech" not in st.session_state:
        st.session_state.user_speech = ""
    
    st.write(f"Record audio. Paste transcribed text in chat.")
    audio = st.audio_input("", label_visibility='collapsed')
    if audio:
        r = sr.Recognizer()
        audio_bytes = audio.getvalue()
        with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
            sample_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            raw_data = wf.readframes(wf.getnframes())
        audio_data = sr.AudioData(raw_data, sample_rate, sample_width)
        try:
            with st.spinner("Please wait...", show_time=True):
                text = r.recognize_google(audio_data)
                text = text.lower()
                st.session_state.user_speech = text
            st.success(f"Recognized: {text}")
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition failed: {e}")
    
    if st.button("Copy to clipboard", key='dialog_copy_btn'):
        pyperclip.copy(st.session_state.user_speech)
        st.rerun()
#-------------------------------------------------------------------------------------------------------------

audio_col, chat_col = st.columns([0.15, 0.85])

with audio_col:
    audio = st.audio_input("", label_visibility='collapsed', key='dialog_audio')

    if audio:
        # Convert recorded audio to speech_recognition-compatible format
        audio_bytes = audio.getvalue()
        with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
            sample_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            raw_data = wf.readframes(wf.getnframes())

        audio_data = sr.AudioData(raw_data, sample_rate, sample_width)

        try:
            text = r.recognize_google(audio_data)
            text = text.lower()
            st.session_state.prompt_placeholder = text
            st.success(f"Recognized: {text}")
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition failed: {e}")

with chat_col:
    prompt = st.chat_input(st.session_state.prompt_placeholder)
    text_area = st.text_area("",value=st.session_state.prompt_placeholder)
    #pyperclip.copy(st.session_state.prompt_placeholder)
    st.toast("Text copied! Paste in chat.")
    
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.chat_message("assistant").markdown(f"Let me answer: **{prompt}**")
        


if st.button("Voice dialog"):
    speech_to_text()


