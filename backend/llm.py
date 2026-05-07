from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

class SimpleLLM:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=150
        )
        
        self.system_prompt = """You are a friendly educational voice assistant.
RULES:
- Always reply in English only, even if user speaks Hindi or other languages
- Keep replies SHORT — max 2 sentences. This is a voice conversation.
- Be warm, encouraging, and helpful
- For the first message, greet the user and ask how their day is going
- Remember what was said earlier in the conversation"""
        
        self.chat_history = []

    def get_response(self, user_text: str) -> str:
        self.chat_history.append(HumanMessage(content=user_text))
        
        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in self.chat_history[-10:]:  # keep last 5 turns
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            else:
                messages.append({"role": "assistant", "content": msg.content})
        
        response = self.llm.invoke(messages).content
        self.chat_history.append(AIMessage(content=response))
        
        print(f"🤖 AI: {response}")
        return response

    def reset(self):
        self.chat_history = []