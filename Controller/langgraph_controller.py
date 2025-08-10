# Coodinates all the agents 
from langgraph.graph import StateGraph
from Agents.ingestion_agent import ingest_agent
from Agents.summarizer_agent import summ_agent
from Agents.QAagent import qaagent
from Controller.controller_logic import classify_prompt_type
from Controller.custom_state import CustomStateType
import os

def ingest_agent_node(state: CustomStateType):
    file_path = state.file_path
    prompt = f"Ingest the document at this path: {file_path}"
    response = ingest_agent.run(prompt)  # Call your Langchain agent here
    state.result = response
    return state

def summ_agent_node(state: CustomStateType):
    file_path = state.file_path
    prompt = f"Summarize the document at this path: {file_path}"
    response = summ_agent.run(prompt)  # Call your Langchain agent here
    state.result = response
    return state

def qa_agent_node(state: CustomStateType):
    file_path = state.file_path
    if file_path:
        file_name = os.path.basename(file_path)
        prompt = state.prompt
        prompt = f"Retrive the document:{file_name} from the vector database, After that answer this question: {prompt}"
        response = qaagent.run(prompt)  # Call your Langchain agent here
        state.result = response
    else:
        prompt = state.prompt
        prompt = f"Anser this question:{prompt}"
        response = qaagent.run(prompt)  # Call your Langchain agent here
        state.result = response
    return state


def create_executor():
    workflow = StateGraph(CustomStateType)

    # Adding all the Nodes: Agents and controller logic
    workflow.add_node("classifier", classify_prompt_type)
    workflow.add_node("ingest", ingest_agent_node)
    workflow.add_node("summarize", summ_agent_node)
    workflow.add_node("QA", qa_agent_node)


    # Setting the entry point of the graph 
    workflow.set_entry_point("classifier")

    # Adding the condition 
    workflow.add_conditional_edges("classifier", lambda state: state.next, {
        "only_file": "summarize",
        "prompt_and_file":"ingest",
        "only_prompt": "QA",
    }
    )

    # Chained node : linked node 
    workflow.add_edge("ingest", "QA")

    # Setting the ending point of the graph
    workflow.set_finish_point("summarize")
    workflow.set_finish_point("QA")

    # Compile graph anr return 
    return workflow.compile()