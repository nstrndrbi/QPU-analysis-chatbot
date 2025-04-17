from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import base64
import os
import tempfile
import uvicorn

from llm_handler import process_query_with_llm
from agent import process_query_with_agent
from data_processor import (
    get_top_active_qpc_blocks, 
    analyze_cost_impact, 
    get_daily_costs, 
    get_qpu_summary,
    get_block_efficiency,
    get_daily_workloads
)
from visualization import generate_trend_graph, generate_workloads_graph, generate_efficiency_graph

app = FastAPI(title="QPU Analysis Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a temp directory for storing generated graphs if it doesn't exist
GRAPH_DIR = os.path.join(tempfile.gettempdir(), "qpu_graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

# Mount static files directory if it exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    use_agent: bool = True  # Flag to use the agent-based approach

class ChatResponse(BaseModel):
    response: str
    graph: Optional[str] = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Process the query using LLM and our tools
        message = request.message.lower()
        response = ""
        graph_b64 = None
        
        # Use the agent-based approach by default
        if request.use_agent:
            response = await process_query_with_agent(request.message, request.history)
            
            # Check if we need to attach a graph
            if "graph" in message or "visualization" in message or "trend" in message:
                if "cost" in message or "daily cost" in message:
                    graph_path = generate_trend_graph()
                    with open(graph_path, "rb") as img_file:
                        graph_b64 = base64.b64encode(img_file.read()).decode('utf-8')
                elif "workload" in message:
                    graph_path = generate_workloads_graph()
                    with open(graph_path, "rb") as img_file:
                        graph_b64 = base64.b64encode(img_file.read()).decode('utf-8')
                elif "efficiency" in message or "ratio" in message:
                    graph_path = generate_efficiency_graph()
                    with open(graph_path, "rb") as img_file:
                        graph_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        else:
            # Direct routing approach (legacy)
            if "top 10 most active QPU blocks" in message:
                top_blocks = get_top_active_qpc_blocks()
                response = f"The top 10 most active QPU blocks by number of workloads executed are:\n\n{top_blocks}"
                
            elif "cost" in message and "atom blocks" in message:
                cost_impact = analyze_cost_impact()
                response = f"If you only use Atom blocks: {cost_impact}"
                
            elif "graph" in message and "trend of daily costs" in message:
                graph_path = generate_trend_graph()
                with open(graph_path, "rb") as img_file:
                    graph_b64 = base64.b64encode(img_file.read()).decode('utf-8')
                response = "Here's the trend of daily costs over time:"
                
            else:
                # Default to LLM for other queries
                response = await process_query_with_llm(request.message, request.history)
        
        return ChatResponse(response=response, graph=graph_b64)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoints for summary data
@app.get("/api/summary", response_model=Dict[str, Any])
async def get_summary():
    """
    Get summary data about QPU blocks and workloads
    """
    try:
        return get_qpu_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/daily_workloads", response_model=List[Dict[str, Any]])
async def get_workloads():
    """
    Get daily workload data
    """
    try:
        return get_daily_workloads()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/efficiency", response_model=List[Dict[str, Any]])
async def get_efficiency():
    """
    Get block efficiency metrics
    """
    try:
        return get_block_efficiency()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/graphs/{graph_type}")
async def get_graph(graph_type: str):
    """
    Get a specific graph
    """
    try:
        graph_path = ""
        if graph_type == "costs":
            graph_path = generate_trend_graph()
        elif graph_type == "workloads":
            graph_path = generate_workloads_graph()
        elif graph_type == "efficiency":
            graph_path = generate_efficiency_graph()
        else:
            raise HTTPException(status_code=400, detail="Invalid graph type")
        
        return FileResponse(graph_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Serve the main HTML application
    """
    html_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return JSONResponse(content={"message": "Welcome to QPU Analysis Chatbot API. Frontend not found."})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
