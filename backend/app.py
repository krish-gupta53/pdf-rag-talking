from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this import
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

# Allow CORS for frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing code
from graph_builder1 import build_agent_graph
from graph_builder2 import build_agent_graphh

@app.post("/pdf-load/")
async def loader(
    user_id: str = Form(...),
    is_pdf_uploaded: bool = Form(...),
    file: Optional[UploadFile] = File(None)
):
    if file is None:
        file_path = "null"
    else:
        file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_pdf")
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    
    state = {
        "is_pdf_uploaded": is_pdf_uploaded,
        "user_message": "",
        "ai_message": "",
        "user_id": user_id,
        "collection_name": f"collect_{user_id}",
        "file_path": file_path,
        "conversation_summary": ""  # Initialize empty summary
    }

    result = build_agent_graph.invoke(state)
    print("result", result)
    return result

@app.post("/pdf-chat/")
async def chatter(
    user_id: str = Form(...),
    user_message: str = Form(...)
):
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_pdf")
    
    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first before asking questions."
        )
    
    state = {
        "is_pdf_uploaded": True,
        "user_message": user_message,
        "ai_message": "",
        "user_id": user_id,
        "collection_name": f"collect_{user_id}",
        "file_path": pdf_path,
        "conversation_summary": ""  # Will be updated by the graph
    }

    result = build_agent_graphh.invoke(state)
    print(result['ai_message'])
    return result
