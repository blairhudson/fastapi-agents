from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Define HTTP Basic Authentication
security_basic = HTTPBasic()

def validate_basic_auth(credentials: HTTPBasicCredentials = Depends(security_basic)):
    """
    Validates the username and password provided using HTTP Basic Auth.
    """
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(status_code=403, detail="Invalid username or password")

# Initialize FastAPIAgents with HTTP Basic Authentication
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_basic_auth)

# Register PydanticAI agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)
