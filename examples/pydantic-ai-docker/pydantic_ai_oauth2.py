from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic_ai import Agent

# Define OAuth2 Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Define a security dependency to validate the token
def validate_token(token: str = Depends(oauth2_scheme)):
    # Replace this with your actual token validation logic
    if token != "valid_token":
        raise HTTPException(status_code=403, detail="Invalid token")

# Configure agent
agent = Agent("openai:gpt-4o-mini")