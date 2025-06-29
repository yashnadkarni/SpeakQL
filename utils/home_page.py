import streamlit as st
import time
from utils.chain import execute_chain
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

# st.title("SpeakQL")
# st.write("Talk to your database. For simple queries")
# ---------- HEADER ----------
st.markdown("<h1 style='text-align: center;'>SpeakQL</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Talk to your database. For simple queries</h5>", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "validate_query" not in st.session_state:
    st.session_state.validate_query = False

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

data = ""
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

@st.dialog("! User Validation")
def human_in_loop(query):
    st.write(f"Procced with query?")
    st.write(query)
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Approve", type='primary'):
            st.session_state.validate_query = True
            st.rerun()
    with col2:
        if st.button("Reject"):
            st.session_state.validate_query = False
            st.rerun()


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
                        st.write(f"SQL query : {step['write_query']['query']}")
                    elif 'execute_query' in step.keys():
                        st.write(f"Database output : {step['execute_query']['result']}")
                    elif 'generate_answer' in step.keys():
                        st.write("Analyzing results")
                        data = step['generate_answer']['answer']
                    time.sleep(2)
                status.update(
                    label="Job complete!", state="complete", expanded=False
                )
        st.write_stream(stream_data(data))
       


    st.session_state.messages.append({"role": "assistant", "content": data})
