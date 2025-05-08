from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from state_schema import State

def upload_pdf(state: State) -> State:
    file_path = state["file_path"]
    collection_name = state["collection_name"]

    # 1. Load the PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(docs)

    # 3. Set up OpenAI Embeddings
    embeddings = OpenAIEmbeddings()

    # 4. Qdrant Client (local or cloud)
    qdrant = QdrantClient(
        url="http://localhost:6333"  # or url="http://localhost:6333" if running server
    )

    # 5. Create collection if not exists
    if collection_name not in qdrant.get_collections().collections:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    # 6. Store in Qdrant
    vectorstore = Qdrant(
        client=qdrant,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    vectorstore.add_documents(chunks)

    # 7. Update state
    state["is_pdf_uploaded"] = True
    state["ai_message"] = f"✅ PDF '{file_path}' uploaded and embedded to Qdrant collection '{collection_name}'."

    return state
