# import os
# import getpass
# import sys
# import io
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.utilities import SQLDatabase
# from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain_core.messages import HumanMessage

# from langchain.chat_models import init_chat_model
# from langchain import hub


# from langgraph.graph import START, StateGraph
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.prebuilt import create_react_agent


# from groq import Groq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# from typing_extensions import TypedDict
# from typing_extensions import Annotated

# from chain import State, QueryOutput, get_api_keys, write_query, execute_query, generate_answer


# api_keys = get_api_keys()

# if not os.environ.get("LANGSMITH_API_KEY"):
#     os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
#     os.environ["LANGSMITH_TRACING"] = "true"

# if not os.environ.get("GROQ_API_KEY"):
#   os.environ["GROQ_API_KEY"] = api_keys["GROQ_API_KEY"]

# db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# llm = init_chat_model("llama3-8b-8192", model_provider="groq")
# query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

# assert len(query_prompt_template.messages) == 2


# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# tools = toolkit.get_tools()
# prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

# assert len(prompt_template.messages) == 1
# system_message = prompt_template.format(dialect="SQLite", top_k=5)
# agent_executor = create_react_agent(llm, tools, prompt=system_message)

# question = "Which country's customers spent the most?"
# output_buffer = io.StringIO()
# original_stdout = sys.stdout
# sys.stdout = output_buffer

# for step in agent_executor.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",):
#    step["messages"][-1].pretty_print()

# sys.stdout = original_stdout
# pretty_output = output_buffer.getvalue()
# st.text_area("Agent Reasoning", pretty_output, height=400)
   

import streamlit as st


if 'temp_text' not in st.session_state:
    st.session_state['temp_text'] = ""

st.session_state['temp_text'] = st.text_input("Enter a text")


st.text_area("Agent Reasoning", st.session_state['temp_text'], height=400)

