import os
import getpass
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langchain import hub
from langchain.chat_models import init_chat_model


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
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY")
    }
    return api_keys

api_keys = get_api_keys()
if not os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_API_KEY"] = api_keys["LANGSMITH_API_KEY"]
    os.environ["LANGSMITH_TRACING"] = "true"

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = api_keys["GROQ_API_KEY"]

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
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


def execute_chain(question):
    graph_builder = StateGraph(State).add_sequence(
        [write_query, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()
    return graph.stream({"question": question}, stream_mode="updates")
