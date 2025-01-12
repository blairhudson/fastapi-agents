from fastapi import FastAPI, Depends, HTTPException, Cookie
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

# Initialize FastAPI app
app = FastAPI()

# Define a cookie-based security dependency
def validate_cookie(session_id: str = Cookie(None)):
    """
    Validates the session ID provided in the cookies.
    """
    if session_id != "valid_session_id":
        raise HTTPException(status_code=403, detail="Invalid or missing session ID")

# Initialize FastAPIAgents with cookie-based security
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_cookie)

# Register PydanticAI agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

# Include the router
app.include_router(agents)

# Endpoint to simulate login and set a cookie
@app.post("/login")
async def login():
    """
    Simulates a login by setting a session ID cookie.
    """
    from fastapi.responses import JSONResponse
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="session_id", value="valid_session_id", httponly=True)
    return response
