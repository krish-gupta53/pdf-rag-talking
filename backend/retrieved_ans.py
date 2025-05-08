from state_schema import State
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, openai_api_key=api_key)
embedding_model = OpenAIEmbeddings()


def retrieved_ans(state: State) -> State:
    # Use the collection specific to the user
    collection_name = state["collection_name"]
    client = QdrantClient(url="http://localhost:6333")
    # Connect to Qdrant with user's collection
    qdrant = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embedding_model
    )

    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=qdrant.as_retriever(),
        llm=llm
    )

    docs = multi_query_retriever.get_relevant_documents(state["user_message"])
    
    # Deduplicate
    seen = set()
    unique_docs = []
    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)

    state["top_chunks"] = unique_docs[:5]  # Add top chunks to state

    return state  # ← Make sure to return a node label and updated state
