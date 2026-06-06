# Standard library imports
import logging
import json
import os
from dotenv import load_dotenv

# Third-party imports
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

load_dotenv(".env")
model = os.getenv("OLLAMA_MODEL")

logging.basicConfig(level=logging.INFO)

if os.getenv('LANGSMITH'):
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ[
        'LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
    os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGSMITH_PROJECT')


def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)


class SqlChain:
    def __init__(self, few_shot_prompts: str, db_uri="sqlite:///data/sqlrag_db", llm_model=model,
                 few_shot_k=2):
        self.llm = ChatOllama(
            model=llm_model, 
            temperature=0
        )
        self.db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=0)
        self.few_shot_k = few_shot_k
        self.few_shot = self._set_up_few_shot_prompts(load_json(few_shot_prompts))
        self.full_prompt = None

        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.tools = toolkit.get_tools()

    def _set_up_few_shot_prompts(self, few_shot_prompts: dict) -> None:
        few_shots = SemanticSimilarityExampleSelector.from_examples(
            few_shot_prompts,
            OllamaEmbeddings(model="qwen3-embedding:0.6b"),
            FAISS,
            k=self.few_shot_k,
            input_keys=["input"],
        )
        return few_shots
    
    def few_prompt_construct(self, query: str, top_k=30, dialect="SQLite") -> str:

        system_prefix = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        ALWAYS query the database before returning an answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return 'I don't know' as the answer.
        DO NOT include information that is not present in the database in your answer.

        Here are some examples of user inputs and their corresponding SQL queries. They are tested and works.
        Use them as a guide when creating your own queries:"""

        # SUFFIX = """Begin!
        #
        #     Question: {input}
        #     Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
        #     I will not stop until I query the database and return the answer.
        #     {agent_scratchpad}"""
        SUFFIX = """Begin!

            Question: {input}
            Thought: I should look at the examples provided and see if I can use them to identify tables and how to build the query.  
            Then I should query the schema of the most relevant tables.
            I will not stop until I query the database and return the answer.
            {agent_scratchpad}"""

        few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.few_shot,
            example_prompt=PromptTemplate.from_template(
                "User input: {input}\nSQL query: {query}"
            ),
            input_variables=["input", "dialect", "top_k"],
            prefix=system_prefix,
            suffix=SUFFIX,
        )
        full_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=few_shot_prompt),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        self.full_prompt = full_prompt.invoke(
            {
                "input": query,
                "top_k": top_k,
                "dialect": dialect,
                "agent_scratchpad": [],
            }
        )

    def prompt_no_few_shot(self, query: str, dialect="SQLite") -> str:
        system_prefix = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return 'I don't know' as the answer.
        DO NOT include information that is not present in the database in your answer."""

        return f"{system_prefix}\n{query}"
    
    def ask(self, query: str, few_prompt: bool = True, rag_test: bool = False):
        if rag_test:
            self.few_prompt_construct(query)
            # Alter the self.full_prompt to only include whats added by the RAG system
            prompt = self.full_prompt.messages
            prompt = prompt[0].content

            prompt = prompt.split("Use them as a guide when creating your own queries:\n\n")[1]
            # Then remove everything after \n\nBegin!\n\n
            prompt = prompt.split("\n\nBegin!\n\n")[0]
            # Split into list of "User input: {input}\nSQL query: {query}"
            prompt = prompt.split("User input: ")
            # Remove the first empty element
            prompt = prompt[1:]
            return prompt

        if few_prompt:
            self.few_prompt_construct(query)
            self.agent = create_agent(
                model=self.llm,
                tools=self.tools,
                system_prompt=self.full_prompt.messages[0].content,
            )
            result = self.agent.invoke({"messages": self.full_prompt.messages})

            # Find the last ToolMessage
            last_context = None
            for msg in result["messages"]:
                if msg.__class__.__name__ == "ToolMessage":
                    last_context = f"{last_context}\n{msg.content}"

            # Find the last AIMessage (final assistant answer)
            final_output = None
            for msg in reversed(result["messages"]):
                if msg.__class__.__name__ == "AIMessage" and msg.content:
                    final_output = msg.content
                    break

            return {
                "retrieved_context": last_context,
                "final_output": final_output
            }

        else:
            self.agent = create_agent(
                model=self.llm,
                tools=self.tools,
                system_prompt=self.full_prompt.messages[0].content,
            )
            result = self.agent.invoke(self.prompt_no_few_shot(query))
            return result, self.prompt_no_few_shot(query)
        

def initialize_agent(few_shot_prompts: str, llm_model="qwen3:0.6b",
                 db_uri="config", few_shot_k=2):
    """ Create an agent with the given few_shot_prompts, llm_model and db_uri
     Call it with agent.ask(prompt)"""
    if db_uri == "config":
        db_uri = os.getenv('DATABASE_PATH')
        db_uri = f"sqlite:///{db_uri}"
        # print(db_uri)
        # print("sqlite:///data/games.db")
        # exit(0)
    return SqlChain(few_shot_prompts, llm_model, db_uri, few_shot_k)


if __name__ == "__main__":
    chain = SqlChain("src/conf/sqls.json")
    res = chain.ask(
        "Is the finance report of Sarawak in the database?",
        rag_test=False
    )

    print("\n=== Retrieved Context (last tool call only) ===")
    print(res["retrieved_context"])

    print("\n=== Final Output ===")
    print(res["final_output"])
    