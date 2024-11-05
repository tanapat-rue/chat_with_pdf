from memory import Memory
from rag import Rag
from langchain_openai import OpenAI


class Assistant:

    def __init__(self) -> None:
        self.llm = OpenAI()
        self.rag = Rag()
        self.memory = Memory()


    def get_response_test(self, prompt):
        messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("user", prompt),
        ]
        response = self.llm.invoke(messages)
        return {"res": response}
    
    def get_response(self, prompt, session_id, refresh=False):
        if refresh:
            self.memory.clear_session(session_id)
        prev_message = self.memory.get_session(session_id)
        messages = []
        for msg in prev_message:
            messages.append((msg.role, msg.message))

        similar_texts = self.rag.query_similar_text(prompt)
        context = "\n".join([f"{idx + 1}. {text}" for idx, (text, _, _) in enumerate(similar_texts)])
        enhanced_prompt = f"Instruction: Please answer the question based on context and response with unknown if the there is no related context. Context: {context}\nQuestion: {prompt}"
        messages.append(("user", enhanced_prompt))
        response = self.llm.invoke(messages)
        self.memory.add_message(session_id=session_id, message=prompt, role="user")
        self.memory.add_message(session_id=session_id, message=response, role="assistant")
        return response