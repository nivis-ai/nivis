from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .agent import VortexAgent
from .tools import get_default_tools

app = FastAPI(
    title="Vortex AI Agent",
    description="A powerful AI agent framework for autonomous task execution",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str
    tools: Optional[List[str]] = None

class QueryResponse(BaseModel):
    status: str
    response: Optional[str] = None
    error: Optional[str] = None

# Initialize agent with default tools
agent = VortexAgent(tools=get_default_tools())

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> Dict[str, Any]:
    """
    Process a query using the Vortex AI Agent
    """
    try:
        result = await agent.run(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
