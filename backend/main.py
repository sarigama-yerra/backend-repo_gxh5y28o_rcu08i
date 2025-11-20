from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from database import db, create_document, get_documents
from schemas import Inquiry

load_dotenv()

app = FastAPI(title="Portfolio API", version="1.0.0")

# CORS
frontend_origin = os.getenv("FRONTEND_URL")
origins = [frontend_origin] if frontend_origin else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/test")
def test():
    status = {
        "backend": "ok",
        "database": "connected" if db is not None else "not_configured",
        "database_url": bool(os.getenv("DATABASE_URL")),
        "database_name": os.getenv("DATABASE_NAME") or None,
        "connection_status": "ok" if db is not None else "missing env",
        "collections": []
    }
    try:
        if db is not None:
            status["collections"] = db.list_collection_names()
    except Exception as e:
        status["connection_status"] = f"error: {e}" 
    return status

@app.post("/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        doc_id = create_document("inquiry", payload)
        return {"id": doc_id, "status": "received"}
    except Exception as e:
        # If DB not available, still respond gracefully
        raise HTTPException(status_code=500, detail=str(e))
