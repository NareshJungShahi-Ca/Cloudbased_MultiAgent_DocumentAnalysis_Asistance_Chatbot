import os
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Extracting metadata
def extract_metadata(file_path:str) -> dict:
    doc = fitz.open(file_path)
    metadata = doc.metadata
    doc.close()
    return metadata

# Splite the text : Chunking 
def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )
    return splitter.create_documents([text])

# Read the uploaded file by pages and splite into chunks 
def extract_text_with_pages(file_path: str):
    doc = fitz.open(file_path)
    chunks = []
    metadatas = []

    for i, page in enumerate(doc):
        text = page.get_text()
        page_chunks = split_text(text)

        for j, chunk in enumerate(page_chunks):
            chunks.append(chunk.page_content)
            metadatas.append({
                "page_number": i + 1,
                "chunk_index_in_page":j,
                "char_start": chunk.metadata.get("start_index", None),
                "char_end": chunk.metadata.get("end_index", None),
                "page_text_length": len(text)
                })
    doc.close()
    return chunks, metadatas

# Store in vector database 
def store_in_vector_db(file_path):
    chunks, page_metadatas = extract_text_with_pages(file_path)
    embedding = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    doc_meta = extract_metadata(file_path)
    filename = os.path.basename(file_path)
    title = doc_meta.get("title") or filename
    creator = doc_meta.get("creator", "Unknown")
    created = doc_meta.get("creationDate", "Unknown")
    metadatas = [
        {
            "page_number": page_meta["page_number"],
            "chunk_index_in_page": page_meta["chunk_index_in_page"],
            "char_start": page_meta["char_start"],
            "char_end": page_meta["char_end"],
            "source_doc": filename,
            "title": title,
            "creator": creator,
            "created": created 
        }
        for chunk, page_meta in zip(chunks, page_metadatas)
        ]

    qdrant = QdrantVectorStore.from_texts(
        texts = chunks,
        embedding = embedding,
        metadatas=metadatas,
        location = os.getenv('QDRANT_HOST'),
        api_key = os.getenv('QDRANT_API_KEY'),
        prefer_grpc = False,
        collection_name="doc_chunks"
    )
    return f"Stored {len(chunks)} chunks in vector DB at Qdrant"


def ingest_document(file_path):
    status = store_in_vector_db(file_path)
    return status  

if __name__ == '__main__':
    response = ingest_document('/Users/nareshjungshahi/Documents/Cloud_Computing/Data/Cloud_computing_project_proposal.pdf')
    print(response)