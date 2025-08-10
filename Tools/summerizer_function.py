""" Tool that extact text and summarize """
import os
import fitz
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url = os.getenv('QDRANT_HOST'),
    api_key= os.getenv('QDRANT_API_KEY')
)

def extract_text(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text() + "/n" 
    doc.close()
    return text

def text_retrival():
    retriver = client.get_collection






