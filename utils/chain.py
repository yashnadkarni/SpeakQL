import os
import getpass
#from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langchain import hub
from langchain.chat_models import init_chat_model


from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command


from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from typing_extensions import TypedDict
from typing_extensions import Annotated

import streamlit as st
import time

# Load environment variables from .env file
#load_dotenv()
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def get_api_keys():
    """Retrieve API keys from environment variables."""
    api_keys = {
        "GROQ_API_KEY": st.secrets["GROQ_API_KEY"],
        "LANGSMITH_API_KEY": st.secrets["LANGSMITH_API_KEY"]
    }
    return api_keys

if "steps" not in st.session_state:
    st.session_state.steps = []

if "validate_query" not in st.session_state:
    st.session_state.validate_query = 0


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

api_keys = get_api_keys()
# if not os.environ.get("LANGSMITH_API_KEY"):
#     os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
#     os.environ["LANGSMITH_TRACING"] = "true"

# if not os.environ.get("GROQ_API_KEY"):
#     os.environ["GROQ_API_KEY"] = api_keys["GROQ_API_KEY"]

db = SQLDatabase.from_uri("sqlite:///data/Chinook.db")
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

def write_query(state: State):
    """Generate SQL query to fetch information."""
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
    assert len(query_prompt_template.messages) == 2
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


def execute_chain(prompt):
    graph_builder = StateGraph(State).add_sequence(
        [write_query, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()
    return graph.stream({"question": prompt}, stream_mode="updates")


# def human_in_loop_for_future(human_in_the_loop=False):
#     st.write(f"Human in loop: {human_in_the_loop}")
#     config = {"configurable": {"thread_id": "1"}}
#     data = "Data: ❌ "
#     graph_builder = StateGraph(State).add_sequence(
#         [write_query, execute_query, generate_answer]
#     )
#     graph_builder.add_edge(START, "write_query")
#     if st.session_state.human_in_the_loop:
#         # Code using human in the loop
#         # with st.empty():
#         #     with st.status("Running SQL Chain...", expanded=True) as status:
#         #         if "graph_interrupted" not in st.session_state:
#         #             st.session_state.graph_interrupted = False
#         #             st.session_state.memory = MemorySaver()
#         #             st.session_state.graph = (
#         #                 StateGraph(State)
#         #                 .add_sequence([write_query, execute_query, generate_answer])
#         #                 .add_edge(START, "write_query")
#         #                 .compile(checkpointer=st.session_state.memory, interrupt_before=["execute_query"])
#         #             )
#         #             st.session_state.config = {"configurable": {"thread_id": "1"}}

#         #             steps = st.session_state.graph.stream(
#         #                 {"question": question},
#         #                 config=st.session_state.config,
#         #                 stream_mode="updates"
#         #             )
#         #             for step in steps:
#         #                 if "write_query" in step:
#         #                     st.session_state.sql = step["write_query"]["query"]
#         #                     st.session_state.graph_interrupted = True
#         #                     break  # pause here for human input
#         #         if st.session_state.graph_interrupted:
#         #             st.write(f"SQL query: `{st.session_state.sql}`")
#         #             st.write("Proceed with execution?")

#         #             col1, col2, col3 = st.columns([0.1,0.1,0.8])
#         #             with col1:
#         #                 if st.button("✅ Approve", use_container_width=True):
#         #                     st.session_state.graph_interrupted = False  # clear flag
#         #                     for step in st.session_state.graph.stream(
#         #                         Command(resume=True),
#         #                         config=st.session_state.config,
#         #                         stream_mode="updates"
#         #                     ):
#         #                         if "generate_answer" in step:
#         #                             st.success("✅ Final Answer:")
#         #                             st.write(step["generate_answer"]["answer"])
#         #                             data = step['generate_answer']['answer']
#         #                             status.update(
#         #                                 label="Job complete!", state="complete", expanded=False
#         #                             )
#         #                             st.write_stream(stream_data(data))
#         #             with col2:
#         #                 if st.button("❌ Reject", use_container_width=True):
#         #                     st.session_state.graph_interrupted = False
#         #                     st.warning("Execution cancelled.")
#         #                     data = "Execution cancelled by user."
#         #                     status.update(
#         #                         label="Execution cancelled by user!", state="error", expanded=False
#         #                     )
#         #                     st.write_stream(stream_data(data))
#         # Initialize session state
#         if question := st.chat_input("Enter your question"):
#             st.session_state.messages.append({"role": "user", "content": question})
#             with st.chat_message("user"):
#                 st.markdown(question)

#             with st.chat_message("assistant"):
#                 if "graph_interrupted" not in st.session_state:
#                     st.session_state.graph_interrupted = False
#                 if "query_approved" not in st.session_state:
#                     st.session_state.query_approved = None

#                 # If not interrupted yet, run first part of graph
#                 if st.session_state.human_in_the_loop and not st.session_state.graph_interrupted:
#                     st.session_state.memory = MemorySaver()
#                     st.session_state.graph = (
#                         StateGraph(State)
#                         .add_sequence([write_query, execute_query, generate_answer])
#                         .add_edge(START, "write_query")
#                         .compile(checkpointer=st.session_state.memory, interrupt_before=["execute_query"])
#                     )
#                     st.session_state.config = {"configurable": {"thread_id": "1"}}

#                     steps = st.session_state.graph.stream(
#                         {"question": question},
#                         config=st.session_state.config,
#                         stream_mode="updates"
#                     )
#                     for step in steps:
#                         if "write_query" in step:
#                             st.session_state.sql = step["write_query"]["query"]
#                             st.session_state.graph_interrupted = True
#                             break

#                 # If interrupted, and no decision yet, ask for approval
#                 if st.session_state.graph_interrupted and st.session_state.query_approved is None:
#                     st.write(f"SQL query: `{st.session_state.sql}`")
#                     st.write("Proceed with execution?")
#                     col1, col2, _ = st.columns([0.1, 0.1, 0.8])
#                     with col1:
#                         if st.button("✅ Approve", use_container_width=True):
#                             st.session_state.query_approved = True
#                     with col2:
#                         if st.button("❌ Reject", use_container_width=True):
#                             st.session_state.query_approved = False

#                 # After decision, handle it on rerun
#                 if st.session_state.query_approved is True:
#                     with st.status("Running SQL Chain...", expanded=True) as status:
#                         for step in st.session_state.graph.stream(
#                             Command(resume=True),
#                             config=st.session_state.config,
#                             stream_mode="updates"
#                         ):
#                             if "generate_answer" in step:
#                                 answer = step["generate_answer"]["answer"]
#                                 status.update(label="✅ Job complete!", state="complete", expanded=False)
#                                 st.success("Final Answer:")
#                                 st.write_stream(stream_data(answer))
#                                 data = answer
#                 elif st.session_state.query_approved is False:
#                     st.warning("❌ Execution cancelled.")
#                     st.write_stream(stream_data("Execution cancelled by user."))
#                     data = "Execution cancelled"

#             st.session_state.messages.append({"role": "assistant", "content": data})
        
#     else:
#         # Code without human in the loop
#         # graph = graph_builder.compile()
#         # for step in graph.stream({"question": question}, stream_mode="updates"):
#         #     if 'write_query' in step.keys():
#         #         st.write(f"SQL query : {step['write_query']['query']}")
#         #     elif 'execute_query' in step.keys():
#         #         st.write(f"Database output : {step['execute_query']['result']}")
#         #     elif 'generate_answer' in step.keys():
#         #         st.write("Analyzing results")
#         #         data = step['generate_answer']['answer']
#         return data
#     #return data


# Questions: How many customers are there in the database, 
 #           What are the names of different artists?