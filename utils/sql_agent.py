import os
import getpass
import streamlit as st
import io
import sys
import time
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langchain import hub


from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from typing_extensions import TypedDict
from typing_extensions import Annotated

# Load environment variables from .env file
load_dotenv()

def get_api_keys():
    """Retrieve API keys from environment variables."""
    api_keys = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY")
    }
    return api_keys



api_keys = get_api_keys()


if not os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_TRACING"] = "true"


db = SQLDatabase.from_uri("sqlite:///data/Chinook.db")

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = api_keys["GROQ_API_KEY"]


llm = init_chat_model("llama3-8b-8192", model_provider="groq")


# Function to capture printed output
def capture_pretty_print(obj):
    buffer = io.StringIO()
    sys.stdout = buffer
    obj.pretty_print()
    sys.stdout = sys.__stdout__
    return buffer.getvalue()

# Building agent ******************************************************
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
# print(tools)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
assert len(prompt_template.messages) == 1

system_message = prompt_template.format(dialect="SQLite", top_k=5)
agent_executor = create_react_agent(llm, tools, prompt=system_message)




# ---------- HEADER ----------
st.markdown("<h1 style='text-align: center;'>SpeakQL Pro</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>For complex queries. Uses a SQL Agent.</h5>", unsafe_allow_html=True)



data = ""
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

prompt = st.chat_input("Enter your question")
if prompt:
    st.write(f"{prompt}")
    output_accum = ""

    with st.status("Running SQL Agent...", expanded=True) as status:
        placeholder = st.empty()
        for step in agent_executor.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            stream_mode="values",):
            output_accum += capture_pretty_print(step["messages"][-1]) + "\n"
            placeholder.code(output_accum, language='text')
        status.update(
            label="Job complete", state="complete", expanded=False
        )

    if step.get("messages")[-1].content:
        final_answer = step["messages"][-1].content
    
    if final_answer:
        st.write_stream(stream_data(final_answer))
    
        




# question = "Which country's customers spent the most?"
# question = "Describe the playlisttrack table"
# How many employees are there?
# What are the unique last names of all employees?
