# rag.py
import os
from pathlib import Path
from typing import List
import pickle
import numpy as np
import faiss
from google import genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

client = genai.Client(api_key=api_key)

# Initialize Google Generative AI
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

KB_PATH = Path(__file__).parent.parent / "kb"
VECTOR_STORE_PATH = Path(__file__).parent / "vector_store.pkl"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

vector_index = None
doc_texts = []

# -----------------------------
# Helper functions
# -----------------------------
def get_embedding(text: str) -> np.ndarray:
    """Get embedding vector from Google Generative AI"""
    
    response = client.models.embed_content(
        model="gemini-embedding-001",   
        contents=[text]
    )
    embedding = response.embeddings[0].values  
    return np.array(embedding, dtype="float32")

def load_kb():
    """Load KB docs and create FAISS index"""
    global vector_index, doc_texts
    docs = []

    for file_path in KB_PATH.glob("*.*"):
        if file_path.suffix.lower() in [".txt", ".md"]:
            docs.append(file_path.read_text(encoding="utf-8"))
        elif file_path.suffix.lower() == ".pdf":
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(str(file_path))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                docs.append(text)
            except Exception as e:
                print(f"⚠️ Failed to read {file_path.name}: {e}")

    doc_texts = []
    for doc in docs:
        doc_texts.extend(text_splitter.split_text(doc))

    embeddings_list = [get_embedding(t) for t in doc_texts]


    # if not embeddings_list:
    #     print("⚠️ No embeddings found. Did you add content to KB files?")
    # return

    vector_index = faiss.IndexFlatL2(len(embeddings_list[0]))
    vector_index.add(np.array(embeddings_list, dtype="float32"))

    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump({"index": vector_index, "texts": doc_texts}, f)

    print(f"✅ KB loaded: {len(doc_texts)} chunks indexed.")
    

def load_vector_store():
    global vector_index, doc_texts
    if VECTOR_STORE_PATH.exists():
        with open(VECTOR_STORE_PATH, "rb") as f:
            data = pickle.load(f)
            vector_index = data["index"]
            doc_texts = data["texts"]
        print(f"✅ Loaded vector store with {len(doc_texts)} chunks.")
    else:
        load_kb()

def query_docs(query: str, top_k: int = 3) -> List[str]:
    global vector_index, doc_texts
    if vector_index is None:
        load_vector_store()

    query_vec = get_embedding(query)
    D, I = vector_index.search(np.array([query_vec], dtype="float32"), top_k)
    return [doc_texts[i] for i in I[0]]

load_vector_store()