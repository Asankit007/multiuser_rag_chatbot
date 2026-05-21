from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
import uuid

from utils.rag_pipeline import process_pdf, embedding_model
from utils.llm import llm

from langchain_community.vectorstores import FAISS

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["rag_app"]

users_collection = db["users"]

class RegisterRequest(BaseModel):
    username: str
    password: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    user_id: str



@app.post("/register")
async def register(request: RegisterRequest):

    existing_user = users_collection.find_one({
        "username": request.username
    })

    if existing_user:
        return {
            "error": "Username already exists"
        }

    user_id = str(uuid.uuid4())

    users_collection.insert_one({
        "username": request.username,
        "password": request.password,
        "user_id": user_id
    })

    return {
        "message": "User registered successfully"
    }

@app.post("/login")
async def login(username: str, password: str):

    user = users_collection.find_one({
        "username": username
    })

    if not user:
        return {
            "error": "User not found"
        }

    if user["password"] != password:
        return {
            "error": "Wrong password"
        }

    return {
        "message": "Login successful",
        "user_id": user["user_id"]
    }








@app.post("/upload-pdf")
async def upload_pdf(user_id: str,file: UploadFile = File(...)):

    user_upload_dir = f"{UPLOAD_DIR}/{user_id}"

    os.makedirs(user_upload_dir, exist_ok=True)

    file_path = f"{user_upload_dir}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = process_pdf(file_path,user_id)

    return {
        "message": "PDF uploaded and processed",
        "chunks": chunks
    }

@app.post("/ask")
async def ask_question(request: QueryRequest):

    vector_path = f"vectordb/{request.user_id}"

    if not os.path.exists(vector_path):
        return {
            "error": "No PDF uploaded for this user."
        }

    vectorstore = FAISS.load_local(
        f"vectordb/{request.user_id}",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(
        request.question,
        k=5
    )

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    prompt = f"""
You are a company HR policy assistant.

Answer ONLY using the provided context.

Rules:
1. Give ONLY the direct answer.
2. Keep the answer under 3 sentences.
3. Do NOT repeat information.
4. Do NOT list unnecessary details.
5. If answer is unavailable, say:
   "I could not find this information in the document."

Context:
{context}

Question:
{request.question}

Answer:
"""

    response = llm.invoke(prompt).content.strip()

    return {
        "question": request.question,
        "answer": response,
        "retrieved_chunks": [
            doc.page_content for doc in docs
        ]
    }