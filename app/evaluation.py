from datasets import Dataset
from pandas import DataFrame
from assistant import Assistant
from rag import Rag
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness,
)

class Evaluation:
    def evaluate_model(self, assistant: Assistant, rag: Rag) -> DataFrame:
        questions = ["Tell me about NL challenges", 
             "What is the component of text-to-SQL prompt?",
             "With the GeoQuery training set, what is the percent accuracy of the finetuned T5?",
             "Tell me about Support Vector Machine",
            ]
        ground_truths = [["Lexical ambiguity, Syntactic ambiguity, Semantic ambiguity, Context-dependent ambiguity"],
                        ["a task instruction, a test database, a test NLQ, and optional demonstrations"],
                        ["The finetuned T5 reaches 87.2% accuracy with the GeoQuery training set"],
                        ["Unknown"]
                        ]
        reference = ["Lexical ambiguity, Syntactic ambiguity, Semantic ambiguity, Context-dependent ambiguity", 
                     "a task instruction, a test database, a test NLQ, and optional demonstrations",
                     "The finetuned T5 reaches 87.2% accuracy with the GeoQuery training set",
                     "Unknown"]
        answers = []
        contexts = []

        # Inference
        for query in questions:
            answers.append(assistant.get_response(prompt=query, session_id="test@mail.com", refresh=True))
            similar_texts = rag.query_similar_text(query)
            context = "\n".join([f"{idx + 1}. {text}" for idx, (text, _, _) in enumerate(similar_texts)])
            contexts.append([context])

        # To dict
        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truths": ground_truths,
            "reference": reference,

        }


        dataset = Dataset.from_dict(data)

        result = evaluate(
            dataset = dataset, 
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall, 
                context_entity_recall, 
                answer_similarity, 
                answer_correctness
            ],
        )
        return result.to_pandas()
        
