# Standard library imports
import os
import argparse
from dotenv import load_dotenv
import csv

# Local imports
from src.embedding_rag import embedding_retriever
from src.extractor import create_extractor
from src.sql_chain import SqlChain
from src.graph_rag import GraphQAAssistant

# Load environment variables
load_dotenv(".env")
llm = os.getenv("OLLAMA_MODEL")
embd_model = os.getenv("EMBEDDING_MODEL")
embdrag_db = os.getenv("EMBDRAG_DATABASE")
sqlrag_db = f"sqlite:///{os.getenv('SQLRAG_DATABASE')}"
schema = os.getenv("SCHEMA")

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Run RAG agents")
parser.add_argument("--sql", action="store_true", help="Run only the SQL agent")
parser.add_argument("--embd", action="store_true", help="Run only the embedding agent")
parser.add_argument("--graph", action="store_true", help="Run only the graph agent")
args = parser.parse_args()

questions = [
    "Is the finance report of Sarawak in the database?",
]


def main():
    # Determine which agents to run
    run_all = not (args.sql or args.embd or args.graph)
    agents = {}

    if args.embd or run_all:
        agents["embd"] = embedding_retriever(embdrag_db, llm, embd_model)
        agents["embd"].embed_metadata()

    if args.sql or run_all:
        extractor = create_extractor(schema, sqlrag_db)
        agents["sql"] = SqlChain("src/conf/sqls.json", sqlrag_db, llm)

    if args.graph or run_all:
        agents["graph"] = GraphQAAssistant(llm)

    # Prepare CSV in append mode
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header only if file is new/empty
        if not file_exists or os.path.getsize("results.csv") == 0:
            writer.writerow(["Question", "Agent", "Retrieved Context", "Final Output"])

        # Run through predefined questions
        for q in questions:
            print(f"\n>>> {q}")

            if "embd" in agents:
                res = agents["embd"].ask(q)
                print("Embedding Agent:", res)
                writer.writerow([q, "Embedding", res["retrieved_context"], res["final_output"]])

            if "sql" in agents:
                clean_q = extractor.clean(q)
                if clean_q:
                    res = agents["sql"].ask(clean_q)
                else:
                    res = agents["sql"].ask(q)
                print("SQL Agent:", res)
                writer.writerow([q, "SQL", res["retrieved_context"], res["final_output"]])

            if "graph" in agents:
                res = agents["graph"].ask(q)
                print("Graph Agent:", res)
                writer.writerow([q, "Graph", res["retrieved_context"], res["final_output"]])

    print("\nResults appended to results.csv")
    exit(0)


if __name__ == "__main__":
    main()