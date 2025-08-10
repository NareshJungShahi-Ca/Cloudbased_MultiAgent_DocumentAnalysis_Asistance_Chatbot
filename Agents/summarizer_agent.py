# Create Summary using LLM 

import os 
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from Tools.All_tool import summarize_document

load_dotenv()


# Large Language Model
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature = 0.2,
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

# Tool for summarization
tools = [summarize_document]

# Creating agent with tools 
summ_agent = initialize_agent(
    tools = tools,
    llm = llm,
    agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose = True
)
