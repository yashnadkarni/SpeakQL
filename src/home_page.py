import streamlit as st
import time
from chain import execute_chain

# st.title("SpeakQL")
# st.write("Talk to your database. For simple queries")
# ---------- HEADER ----------
st.markdown("<h1 style='text-align: center;'>SpeakQL</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Talk to your database. For simple queries</h5>", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

data = ""
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)


if prompt := st.chat_input("Enter your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        graph_stream = execute_chain(prompt)
        with st.empty():
            with st.status("Running SQL Chain...", expanded=True) as status:
                for step in graph_stream:
                    if 'write_query' in step.keys():
                        st.write(f"Running SQL query : {step['write_query']['query']}")
                    elif 'execute_query' in step.keys():
                        st.write(f"Database output : {step['execute_query']['result']}")
                    elif 'generate_answer' in step.keys():
                        st.write("Analyzing results")
                        data = step['generate_answer']['answer']
                    # time.sleep(2)
                status.update(
                    label="Job complete!", state="complete", expanded=False
                )
        st.write_stream(stream_data(data))
    st.session_state.messages.append({"role": "assistant", "content": data})
