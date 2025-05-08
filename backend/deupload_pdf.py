import os
from qdrant_client import QdrantClient
from state_schema import State

def deupload_pdf(state: State) -> State:
    file_path = f"uploads/{state["user_id"]}_pdf"
    collection_name = f"collect_{state["user_id"]}"

    # 1. Delete the uploaded file from the filesystem
    if os.path.exists(file_path):
        os.remove(file_path)
        file_deleted = True
    else:
        file_deleted = False

    # 2. Connect to Qdrant and delete the collection
    qdrant = QdrantClient(url="http://localhost:6333")  # use url=... for remote
    collections = qdrant.get_collections().collections
    if any(col.name == collection_name for col in collections):
        qdrant.delete_collection(collection_name=collection_name)
        collection_deleted = True
    else:
        collection_deleted = False

    # 3. Update state
    state["is_pdf_uploaded"] = False
    state["ai_message"] = (
        f"🗑️ Deleted collection '{collection_name}' from Qdrant. "
        f"{'Removed PDF file.' if file_deleted else 'File not found.'}"
    )
    state["collection_name"]= "" 
    state["file_path"]= ""
    

    return state
