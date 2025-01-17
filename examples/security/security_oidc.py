from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OpenIdConnect
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Define OpenID Connect security
oidc_scheme = OpenIdConnect(openIdConnectUrl="https://example.com/.well-known/openid-configuration")

def validate_openid_token(token: str = Depends(oidc_scheme)):
    """
    Validates the OpenID Connect token.
    Replace this logic with your identity provider's token validation.
    """
    if token != "valid_openid_token":
        raise HTTPException(status_code=403, detail="Invalid OpenID Connect token")

# Initialize FastAPIAgents with OpenID Connect security
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_openid_token)

# Register PydanticAI agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)
