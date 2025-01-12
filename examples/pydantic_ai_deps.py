from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.security import APIKeyHeader
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic import BaseModel
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key")

# Define API key validation
def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "my-secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Initialize FastAPIAgents with security
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_api_key)

# Define the structure of the dependencies
class MyDepsModel(BaseModel):
    api_key: str
    user_agent: str

# Initialize the Agent with `deps_type`
agent = Agent("openai:gpt-4o-mini", deps_type=MyDepsModel)

# Use the dependencies directly in the agent
# ...

# Refactored runtime dependency resolution logic
async def resolve_deps(
    api_key: str = Depends(api_key_header),  # Use validated API key from `api_key_header`
    user_agent: str = Header("Unknown-Agent"),  # Extract User-Agent header
):
    """
    Resolves runtime dependency values based on request context.
    """
    return {
        "api_key": str(api_key),  # Use the validated API key directly
        "user_agent": str(user_agent),  # Extract User-Agent header value
    }

# Register the PydanticAI agent
pydantic_ai_agent = PydanticAIAgent(agent=agent, deps=resolve_deps)
agents.register("pydanticai", pydantic_ai_agent, tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)
