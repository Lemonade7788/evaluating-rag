# Standard library imports
import streamlit as st
from dotenv import load_dotenv
import os

# Local imports
from src.embedding_rag import embedding_retriever
from src.sql_chain import SqlChain
from src.graph_rag import GraphQAAssistant

# Load environment variables once
load_dotenv(".env")
llm = os.getenv('OLLAMA_MODEL')
embd_model = os.getenv("EMBEDDING_MODEL")
embdrag_db = os.getenv("EMBDRAG_DATABASE")
sqlrag_db = f"sqlite:///{os.getenv('SQLRAG_DATABASE')}"

# --- Cache initialization ---
@st.cache_resource
def init_embedding_agent():
    agent = embedding_retriever(embdrag_db, llm, embd_model)
    agent.embed_metadata()   # expensive step, run once
    return agent

@st.cache_resource
def init_sql_agent():
    return SqlChain("src/conf/sqls.json", sqlrag_db, llm)

@st.cache_resource
def init_graph_agent():
    return GraphQAAssistant(llm)

# Initialize agents only once
embedding_agent = init_embedding_agent()
sql_agent = init_sql_agent()
graph_agent = init_graph_agent()

# --- Streamlit UI ---
st.set_page_config(page_title="RAG Chatbot", layout="centered")

st.title("💬 RAG Chatbot Assistant")
st.write("Select a query and get a response from your chosen RAG strategy.")

# Sidebar for agent selection
st.sidebar.header("⚙️ Choose RAG Strategy")
agent_choice = st.sidebar.radio(
    "Select Agent:",
    ["Embedding-RAG", "SQL-RAG", "Graph-RAG"]
)

st.sidebar.write(f"LLM Model: `{llm}`")
st.sidebar.write(f"Embedding Model: `{embd_model}`")
st.sidebar.write(f"Embedding DB: `{embdrag_db}`")
st.sidebar.write(f"SQL DB: `{sqlrag_db}`")

# Preset queries
preset_queries = [
    "Is the finance report of Sarawak in the database?",
    "Are Kuching and Lundu in the database?",
    "What is the price of Nipah Sugar in March 1971 in Kuching?",
    "How many pupils entered the exam in Lundu in 1969?",
    "Did Lawas or Sundar have the highest import expenditure in 1969?",
    "Between fresh duck egg and salted duck egg, which was more expensive in July 1971?",
    "List all events in August 1971.",
    "List all administrative staffs that were transfered to Kapit in 1970.",
    "Calculate the inflation rate of tea from July to November of 1971.",
    "Calculate the increase in Sarawak revenue from 1907 to 1927.",
    "Other..."
]

# Centered input
selected = st.selectbox("Choose a query:", options=preset_queries, index=None, key="preset_query")
if selected == "Other...":
    user_query = st.text_input("Or type your own query:", key="custom_query")
else:
    user_query = selected

# Response area
if user_query:
    st.markdown("---")
    st.subheader("🤖 Response")

    if agent_choice == "Embedding-RAG":
        response = embedding_agent.ask(user_query)
    elif agent_choice == "SQL-RAG":
        response = sql_agent.ask(user_query)
    else:
        response = graph_agent.ask(user_query)

    st.write(response["final_output"])
