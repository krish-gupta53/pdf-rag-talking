from typing import List, Optional
from typing_extensions import TypedDict
from langchain.schema import Document

class State(TypedDict):
    is_pdf_uploaded: bool
    user_message: str
    ai_message: str
    user_id: str
    collection_name: str
    file_path: str  
    top_chunks: List[Document]