from state_schema import State
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, openai_api_key=api_key)

# Dictionary to store memory for each user
user_memories = {}

# Initial system prompt to guide the LLM's behavior
system_prompt = """
You are a helpful assistant. Use the provided context from the uploaded PDF and conversation history to answer the user's question accurately. 
If the answer is not in the context, say "I couldn't find the answer in the document."
Maintain consistency with previous responses and acknowledge the conversation history when relevant.
"""

def get_user_memory(user_id: str) -> ConversationBufferMemory:
    """
    Get or create a conversation memory for a specific user.
    """
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return user_memories[user_id]

def llm_response(state: State) -> State: 
    user_question = state["user_message"]
    top_chunks = state.get("top_chunks", [])
    user_id = state["user_id"]

    context = "\n\n".join([doc.page_content for doc in top_chunks])
    
    # Get conversation history from user-specific memory
    memory = get_user_memory(user_id)
    chat_history = memory.load_memory_variables({})["chat_history"]
    
    # Include conversation history in the context
    full_context = f"""
    PDF Context:
    {context}
    """

    messages = [
        SystemMessage(content=system_prompt),
        *chat_history,  # Add conversation history
        HumanMessage(content=f"Context:\n{full_context}\n\nQuestion:\n{user_question}")
    ]

    response = llm(messages).content
    state["ai_message"] = response
    
    # Save the interaction to user-specific memory
    memory.save_context({"input": user_question}, {"output": response})
    
    return state
