from fastapi import HTTPException

# Custom Exceptions
class AgentNotFoundError(HTTPException):
    def __init__(self, agent_name: str):
        super().__init__(status_code=404, detail=f"Agent '{agent_name}' not found")

class InvalidPayloadError(ValueError):
    def __init__(self, message: str = "Invalid payload provided"):
        super().__init__(message)
