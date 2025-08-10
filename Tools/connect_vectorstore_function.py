"""Function that connects the vector database"""
import os
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

def connect_vectorstore():
    # Loading the same embedding model that embed the pdf chunks 
    embedding = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    # Defining the client 
    client = QdrantClient(
        url = os.getenv("QDRANT_HOST"),
        api_key = os.getenv("QDRANT_API_KEY")
    )
    # Connecting 
    qdrant  = QdrantVectorStore(
        client = client,
        embedding = embedding,
        collection_name="doc_chunks"
    )
    return qdrant
