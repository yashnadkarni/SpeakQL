import os
import getpass
import streamlit as st
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

# def main():
#     try:
#         # Get API keys
#         api_keys = get_api_keys()
        
#         if not api_keys["GROQ_API_KEY"]:
#             raise ValueError("GROQ_API_KEY not found in environment variables")

#         # Set up LangSmith if API key is available
#         if api_keys["LANGSMITH_API_KEY"]:
#             os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
#             os.environ["LANGSMITH_TRACING"] = "true"

#         # Use the correct path to the database file
#         db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Chinook.db")
#         if not os.path.exists(db_path):
#             raise FileNotFoundError(f"Database file not found at {db_path}")

#         # Connect to the database
#         db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
#         # Test database connection
#         print("Database dialect:", db.dialect)
#         print("\nAvailable tables:", db.get_usable_table_names())
#         print("\nSample query result:", db.run("SELECT * FROM Artist LIMIT 3;"))

#         # Create a Groq client
#         client = Groq(
#             api_key=api_keys["GROQ_API_KEY"]
#         )

#         from typing_extensions import TypedDict


#         class State(TypedDict):
#             question: str
#             query: str
#             result: str
#             answer: str

#         # Your Streamlit app code will go here
#         # st.title("SQL Agent with Groq")
#         # st.write("Connected to database successfully!")

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         if st._is_running:
#             st.error(f"Error: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()






api_keys = get_api_keys()


if not os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_TRACING"] = "true"


db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM Artist LIMIT 10;"))

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = api_keys["GROQ_API_KEY"]


llm = init_chat_model("llama3-8b-8192", model_provider="groq")




query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

assert len(query_prompt_template.messages) == 2
for message in query_prompt_template.messages:
    message.pretty_print()

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information."""
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

#print(write_query({"question": "How many Employees are there?"}))
#print(write_query({"question": input("Enter question: ")}))

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

# res = execute_query({"query": "SELECT COUNT(EmployeeId) AS EmployeeCount FROM Employee;"})
# print(res)

# temp_query = write_query({"question": "What are unique last names of all employees?"})
# a = execute_query(temp_query)
#print(a)

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




# graph_builder = StateGraph(State).add_sequence(
#     [write_query, execute_query, generate_answer]
# )
# graph_builder.add_edge(START, "write_query")
# graph = graph_builder.compile()

# # Just to show flow of execution
# # from IPython.display import Image, display
# # display(Image(graph.get_graph().draw_mermaid_png()))


# for step in graph.stream({"question": "How many employees are there?"}, stream_mode="updates"):
#     print(step)



# Adding a checkpoint( MemorySaver) ******************************************************
# memory = MemorySaver()
# graph = graph_builder.compile(checkpointer=memory, interrupt_before=["execute_query"])

# # Now that we're using persistence, we need to specify a thread ID
# # so that we can continue the run after review.
# config = {"configurable": {"thread_id": "1"}}

# for step in graph.stream(
#     {"question": "How many employees are there?"},
#     config,
#     stream_mode="updates",
# ):
#     print(step)

# try:
#     user_approval = input("Do you want to go to execute query? (yes/no): ")
# except Exception:
#     user_approval = "no"

# if user_approval.lower() == "yes":
#     # If approved, continue the graph execution
#     for step in graph.stream(None, config, stream_mode="updates"):
#         print(step)
# else:
#     print("Operation cancelled by user.")
# Checkpoint end ******************************************************

# Building agent ******************************************************
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

# print(tools)


prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
prompt_template.messages[0].pretty_print()

system_message = prompt_template.format(dialect="SQLite", top_k=5)



agent_executor = create_react_agent(llm, tools, prompt=system_message)

# question = "Which country's customers spent the most?"

# for step in agent_executor.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()


st.title("SQL Agent")

question = st.text_input("Enter your question: ")

if st.button("Submit"):
    # for step in agent_executor.stream(
    #     {"messages": [{"role": "user", "content": question}]},
    #     stream_mode="values",):
    #     st.text_area("Response", step["messages"][-1].content, height=300)
    
    log_container = st.empty()
    log_text = ""
    for step in agent_executor.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",):        
        #log_container.text_area("Logs", step["messages"][-1].content, height=400)
        st.write(step["messages"][-1].content)
        





# question = "Describe the playlisttrack table"

# for step in agent_executor.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()