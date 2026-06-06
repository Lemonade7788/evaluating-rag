import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class Evaluator:
    def __init__(self, model_name="gemma4:31b-cloud", temperature=0.0):
        # Deterministic output
        self.llm = ChatOllama(model=model_name, temperature=temperature)

    def _invoke(self, prompt: str) -> float:
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return float(response.content.strip())

    def evaluate_context_relevance(self, query: str, context: str) -> float:
        prompt = f"""
        Evaluate the relevance of the context to the query.

        Scoring rubric:
        - 1.000 = fully relevant, directly answers query
        - 0.700–0.999 = strongly relevant, useful but not complete
        - 0.400–0.699 = somewhat relevant, partial support
        - 0.100–0.399 = weak relevance, tangential
        - 0.000–0.099 = irrelevant

        Return only a numeric score with three decimal places.

        Query: {query}
        Context: {context}
        """
        return self._invoke(prompt)

    def evaluate_groundedness(self, response_text: str, context: str) -> float:
        prompt = f"""
        Evaluate how well each claim in the response is supported by the retrieved context.

        Scoring rubric:
        - 1.000 = all claims fully supported by the context
        - 0.700–0.999 = most claims supported, minor gaps
        - 0.400–0.699 = some claims supported, significant gaps
        - 0.100–0.399 = few claims supported, mostly unsupported
        - 0.000–0.099 = no claims supported, completely ungrounded

        Return only a numeric score with three decimal places.

        Response: {response_text}
        Context: {context}
        """
        return self._invoke(prompt)

    def evaluate_answer_relevance(self, query: str, response_text: str) -> float:
        prompt = f"""
        Evaluate how well the final response directly answers the original query.

        Scoring rubric:
        - 1.000 = fully relevant, directly and completely answers the query
        - 0.700–0.999 = strongly relevant, answers most aspects but not fully complete
        - 0.400–0.699 = somewhat relevant, partially answers the query
        - 0.100–0.399 = weak relevance, tangential or incomplete answer
        - 0.000–0.099 = irrelevant, does not answer the query at all

        Return only a numeric score with exactly three decimal places.

        Query: {query}
        Response: {response_text}
        """
        return self._invoke(prompt)


def evaluate_csv(input_csv: str, output_csv: str):
    evaluator = Evaluator()
    df = pd.read_csv(input_csv)

    # Add new columns for scores
    df["Context Relevance"] = df.apply(
        lambda row: evaluator.evaluate_context_relevance(row["Question"], row["Retrieved Context"]), axis=1
    )
    df["Groundedness"] = df.apply(
        lambda row: evaluator.evaluate_groundedness(row["Final Output"], row["Retrieved Context"]), axis=1
    )
    df["Answer Relevance"] = df.apply(
        lambda row: evaluator.evaluate_answer_relevance(row["Question"], row["Final Output"]), axis=1
    )

    # Save results
    df.to_csv(output_csv, index=False)
    print(f"Evaluation complete. Results saved to {output_csv}")


# Example usage
if __name__ == "__main__":
    evaluate_csv("results.csv", "evaluated_output.csv")