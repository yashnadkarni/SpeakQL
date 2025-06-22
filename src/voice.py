import streamlit as st
import speech_recognition as sr
import wave
import io
import pyperclip

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
            st.info(f"{text}")
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition failed: {e}")
    
    if st.button("Copy to clipboard", key='dialog_copy_btn'):
        pyperclip.copy(st.session_state.user_speech)
        st.rerun()
#-------------------------------------------------------------------------------------------------------------
