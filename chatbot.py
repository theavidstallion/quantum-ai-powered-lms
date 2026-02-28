"""
Flask-compatible Student Chatbot using LangChain + Groq
"""
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class ChatHistory:
    """Simple chat history storage"""
    def __init__(self):
        self.store = {}
    
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

class StudentChatbot:
    """AI Academic Assistant for University Students"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=self.api_key,
            temperature=0.7
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are QUANTUM ASSISTANT, a helpful academic assistant for university students.
Help with: grades, courses, study tips, academic questions, and university life.
Be friendly, supportive, and encouraging. Keep responses concise and clear.
If asked about math or science, explain step by step.
End every response with a short encouraging line."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm
        self.history = ChatHistory()
        
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,
            self.history.get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    
    def chat(self, message: str, session_id: str = "default") -> str:
        """Process a chat message and return response"""
        # Auto-detect subject type
        msg_lower = message.lower()
        if any(word in msg_lower for word in ['math', 'algebra', 'calculus', 'equation', 'solve']):
            message = f"Solve step by step: {message}"
        
        try:
            response = self.chain_with_history.invoke(
                {"input": message},
                config={"configurable": {"session_id": session_id}}
            )
            return response.content
        except Exception as e:
            return f"I'm having trouble connecting right now. Please try again. Error: {str(e)}"
