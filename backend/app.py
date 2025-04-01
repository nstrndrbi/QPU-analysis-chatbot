from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import base64
import uvicorn

from llm_handler import process_query_with_llm
from data_processor import get_top_active_qpc_blocks, analyze_cost_impact, get_daily_costs
from visualization import generate_trend_graph

app = FastAPI(title="QPC Analysis Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

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
        
        if "top 10 most active qpc blocks" in message:
            top_blocks = get_top_active_qpc_blocks()
            response = f"The top 10 most active QPC blocks by number of workloads executed are:\n\n{top_blocks}"
            
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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
