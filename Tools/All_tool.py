
from langchain.tools import tool
from Tools.document_ingestion_function import ingest_document
from Tools.summerizer_function import extract_text
from Tools.connect_vectorstore_function import connect_vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA 
import os
from dotenv import load_dotenv

load_dotenv()

# Large Language Model 
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature = 0.2,
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

@tool
def ingest_pdf(file_path: str) -> str:
    """Ingest a PDF and store it in vector database and prepare it for summarization and Q&A."""
    print(f"DEBUG: ingest received file_path: {file_path}")
    return ingest_document(file_path)

@tool
def summarize_document(file_path: str) -> str:
    """Summarizing PDF document by exrating the text from the PDF"""
    print(f"DEBUG: Summarizer received file_path: {file_path}")
    full_text = extract_text(file_path)
    prompt = f"Summarize this documnet:\n\n{full_text}"
    summary  = llm.invoke(prompt)
    return summary

@tool
def QA_tool(query: str ) -> str:
    """Answer all the question"""
    connect = connect_vectorstore()
    qa_chain = RetrievalQA.from_chain_type(
        llm = llm, 
        retriever = connect.as_retriever()
    )
    response = qa_chain.run(query)
    return response





