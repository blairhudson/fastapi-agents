from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Token endpoint
@app.post("/token")
async def token_endpoint(username: str = Form(...), password: str = Form(...)):
    """
    Token endpoint to authenticate users and issue tokens.
    Expects username and password as form data.
    """
    # Validate username and password
    if username == "user" and password == "pass":
        return {"access_token": "valid_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Define OAuth2 Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Define a security dependency to validate the token
def validate_token(token: str = Depends(oauth2_scheme)):
    # Replace this with your actual token validation logic
    if token != "valid_token":
        raise HTTPException(status_code=403, detail="Invalid token")

# Initialize FastAPIAgents with global security
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_token)

# Register PydanticAI agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)

