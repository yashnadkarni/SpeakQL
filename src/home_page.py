import streamlit as st
import time

st.title("SpeakQL")
st.write("Talk to your database - a SQL agent app")
#st.text_input("Add database URI ", key='db_uri', value='sqlite:///Chinook.db')
#sqlite:///Chinook.db
temp_random_text = """
Lorem ipsum dolor sit amet, elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""
def stream_data():
    for word in temp_random_text.split(" "):
        yield word + " "
        time.sleep(0.02)

prompt = st.chat_input("Enter your question")
if prompt:
    st.write(f"{prompt}")
    st.write_stream(stream_data)
    with st.status("Running SQL Agent...", expanded=True) as status:
        st.write("Converting to SQL query")
        time.sleep(2)
        st.write("Querying database")
        time.sleep(1)
        st.write("Analyzing results")
        time.sleep(1)
        status.update(
            label="Job complete!", state="complete", expanded=False
        )
    st.write_stream(stream_data)