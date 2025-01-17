from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Define API Key security
api_key_header = APIKeyHeader(name="X-API-Key")

def validate_api_key(api_key: str = Depends(api_key_header)):
    """
    Validates the API key provided in the X-API-Key header.
    """
    if api_key != "my-secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Initialize FastAPIAgents with API Key security
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_api_key)

# Register PydanticAI agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)
