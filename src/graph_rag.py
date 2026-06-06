# Standard library imports
from dotenv import load_dotenv
import os

# Third-party imports
from langchain_ollama import ChatOllama
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate

class GraphQAAssistant:
    def __init__(self, model="gemma4:31b-cloud"):
        load_dotenv()
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        self.graph = Neo4jGraph(url=uri, username=username, password=password)
        self.llm = ChatOllama(model=model, temperature=0)
        self.schema = self.graph.get_schema

        # Cypher generation prompt now includes triplets
        self.cypher_prompt = PromptTemplate(
            input_variables=["question", "schema", "triplets"],
            template="""You are an expert Cypher query generator.

Schema:
{schema}

Relevant relational triplets extracted from the query:
{triplets}

Question:
{question}

Rules:
- Only use labels and properties from the schema above.
- Use the relational triplets as a reference for which entities and relationships to query.
- Query other relevant entities if necessary.
- Always produce simple Cypher only.
- Do not invent fields or labels.
- Do not comment.
- Avoid defining variables sterting with numbers.
Cypher:"""
        )

        self.chain = GraphCypherQAChain.from_llm(
            self.llm,
            graph=self.graph,
            verbose=True,
            allow_dangerous_requests=True,
            return_intermediate_steps=True,
            cypher_prompt=self.cypher_prompt,
            top_k = 30
        )

        self.final_prompt = PromptTemplate(
            input_variables=["question", "cypher", "context"],
            template="""
You are an assistant that answers questions using Neo4j graph data.

Question:
{question}

Generated Cypher Query:
{cypher}

Full Context (query results):
{context}

Instructions:
- Always refer to BOTH the Cypher query and the full context when answering.
- The Cypher query shows how the data was retrieved.
- The context contains the actual results from the database.
- Use the context directly to form the answer. Do not speculate.
- If results exist, list them clearly. If no results exist, say so explicitly.
"""
        )

    def extract_triplets_from_query(self, question: str):
        """Extract relational triplets from the user query, grounded in the schema."""
        triplet_prompt = f"""
        You are an expert in graph schema analysis.

        Schema:
        {self.schema}

        User Query:
        {question}

        Task:
        - Identify all possible relational triplets implied by the query.
        - Each triplet should be in the form (Entity1)-[RELATION]->(Entity2).
        - Only use labels and relationships that exist in the schema.
        - Return them as a JSON list of objects with keys: source, relation, target.
        """
        response = self.llm.invoke(triplet_prompt)
        return response.content.strip()

    def ask(self, question: str):
        # Step 1: Extract triplets
        triplets = self.extract_triplets_from_query(question)
        print(triplets)

        # Step 2: Run the chain with triplets included
        result = self.chain.invoke({
            "query": question,
            "schema": self.schema,
            "triplets": triplets
        })

        cypher_query = result["intermediate_steps"][0]["query"]
        query_context = result["intermediate_steps"][1]["context"]

        prompt_text = self.final_prompt.format(
            question=question,
            cypher=cypher_query,
            context=query_context
        )

        ai_msg = self.llm.invoke(prompt_text)
        return {
            "retrieved_context": f"Cypher used:\n{cypher_query}\n\nContext:\n{query_context}",
            "final_output": ai_msg.content
        }


if __name__ == "__main__":
    assistant = GraphQAAssistant()
    response = assistant.ask("List all events in August 1971.")
    print("\n=== Retrieved Context (last tool call only) ===")
    print(response["retrieved_context"])

    print("\n=== Final Output ===")
    print(response["final_output"])