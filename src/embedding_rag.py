# Standard library imports
from dotenv import load_dotenv
import os
import sqlite3
from typing import List, Tuple
import json

# Third-party imports
from langchain_ollama import ChatOllama, OllamaEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent

load_dotenv(".env")

if os.getenv('LANGSMITH'):
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ[
        'LANGCHAIN_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
    os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGSMITH_PROJECT')


class EmbeddingRAG:
    def __init__(self, db_path="db", llm_model="gemma4:31b-cloud", embd_model="qwen3-embedding:0.6b"):
        self.llm = ChatOllama(
            model=llm_model, 
            temperature=0.8,
        )
        self.embeddings = OllamaEmbeddings(model=embd_model)

        # Build FAISS index
        embedding_dim = len(self.embeddings.embed_query("hello world"))
        index = faiss.IndexFlatL2(embedding_dim)
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        self.db_path = db_path

        # Register tools and agent
        self.tools = [self.retrieve_context]
        prompt = (
            "You have access to a tool that retrieves context from historical tables "
            "extracted from the Sarawak Gazette. Use the tool to help answer user queries "
            "by grounding your responses in the retrieved descriptions."
        )
        self.agent = create_agent(self.llm, self.tools, system_prompt=prompt)

    def get_table_rows(self, table_name: str):
        """
        Fetch all rows from a given table in the SQLite database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def embed_metadata(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all rows from Metadata
        cursor.execute("SELECT table_name, description FROM Metadata;")
        rows = cursor.fetchall()
        conn.close()

        # Add each description to the vector store
        for table_name, description in rows:
            # Create embedding
            self.vector_store.add_texts(
                texts=[description],
                metadatas=[{"table_name": table_name}]
            )

        print(f"Embedded {len(rows)} descriptions into the vector store.")

    def retrieve_context(self, query: str):
        """Retrieve information to help answer a query."""
        retrieved_docs = self.vector_store.similarity_search(query, k=2)
        closest_table = retrieved_docs[0].metadata.get("table_name")
        rows = self.get_table_rows(closest_table)
        
        serialized = (
            f"Closest table: {closest_table}\n\n"
            f"Description: {retrieved_docs[0].page_content}\n\n"
            f"All rows:\n"
        )
        for row in rows:
            serialized += f"{row}\n"

        return serialized, retrieved_docs
    
    def expand_query(self, query: str, num_expansions: int = 3) -> List[str]:
        """Expand the query into related variations (including the original)."""
        expansion_prompt = (
            f"Expand the following query into {num_expansions} semantically related variations. "
            "Do not add any additional information. "
            f"Keep them concise and relevant to historical context.\n\n"
            f"Query: {query}\n\n"
            f"Return only the expanded queries as a JSON list of strings."
        )
        response = self.llm.invoke(expansion_prompt)
        try:
            expansions = json.loads(response.content)
            if isinstance(expansions, list):
                return [query] + expansions
        except Exception:
            expansions = response.content.strip().split("\n")
            return [query] + [e.strip() for e in expansions if e.strip()]
        return [query]

    def retrieve_best_tables(self, query: str, k: int = 5, top_n: int = 1) -> List[Tuple[str, str, float]]:
        """
        Retrieve across expanded queries and return the top N best tables.
        Returns a list of (table_name, description, score).
        """
        expanded_queries = self.expand_query(query)
        print("Expanded Queries: ", expanded_queries)
        all_results = []

        for q in expanded_queries:
            docs = self.vector_store.similarity_search_with_score(q, k=k)
            for doc, score in docs:
                all_results.append((doc.metadata.get("table_name"), doc.page_content, score))

        # Deduplicate by table_name, keeping best score
        best_results = {}
        for table, desc, score in all_results:
            if table not in best_results or score < best_results[table][2]:
                best_results[table] = (table, desc, score)

        # Sort by score (lower = closer in FAISS)
        merged = sorted(best_results.values(), key=lambda x: x[2])
        return merged[:top_n]

    def ask(self, query: str):
        result = self.agent.invoke({"messages": [{"role": "user", "content": query}]})

        last_context = None

        # Iterate through messages and overwrite whenever a tool is called
        for msg in result["messages"]:
            if hasattr(msg, "name") and msg.name == "retrieve_context":
                last_context = msg.content  # always keep the latest tool output

        # The final output is always the last message
        final_output = result["messages"][-1].content

        return {
            "retrieved_context": last_context,
            "final_output": final_output
        }


def embedding_retriever(db_path="db", llm_model="gemma4:31b-cloud", embd_model="qwen3-embedding:0.6b"):
    return EmbeddingRAG(db_path, llm_model, embd_model)


if __name__ == "__main__":
    agent = EmbeddingRAG(db_path="db", llm_model="gemma4:31b-cloud")
    agent.embed_metadata()

    result = agent.ask("List all events in August 1971.")

    print("\n=== Retrieved Context ===")
    print(result["retrieved_context"])

    print("\n=== Final Output ===")
    print(result["final_output"])