import streamlit as st
import time

st.set_page_config(page_title="SpeakQL for Enterprise", layout="wide", page_icon="🗣️")

# Create a placeholder for the changing title
title_placeholder = st.empty()
st.markdown("<h4 style='text-align: center;'>Conversational SQL Interface for Enterprise Data Teams</h4>", unsafe_allow_html=True)
st.markdown("---")

# Optional: run animation once with a button
if st.button("▶ Animate Title"):
    for word in ["Teams", "Organizations", "Enterprise", "You"]:
        title_placeholder.markdown(
            f"<h1 style='text-align: center;'>🗣️ SpeakQL for {word}</h1>",
            unsafe_allow_html=True
        )
        time.sleep(1.2)
    # Final title stays at "You"
else:
    title_placeholder.markdown(
        f"<h1 style='text-align: center;'>🗣️ SpeakQL for You</h1>",
        unsafe_allow_html=True
    )
