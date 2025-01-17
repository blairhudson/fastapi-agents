from fastapi import HTTPException

# Custom Exceptions
class AgentNotFoundError(HTTPException):
    """
    Exception raised when an agent is not found in the registry.
    
    Args:
        agent_name (str): The name of the agent that was not found.

    Returns:
        AgentNotFoundError: An instance of the AgentNotFoundError exception.

    """
    def __init__(self, agent_name: str):
        super().__init__(status_code=404, detail=f"Agent '{agent_name}' not found")

class InvalidPayloadError(ValueError):
    """
    Exception raised when an invalid payload is provided to an agent.

    Args:
        message (str, optional): The error message to display. Defaults to "Invalid payload provided".
    
    Returns:
        InvalidPayloadError: An instance of the InvalidPayloadError exception.

    """
    def __init__(self, message: str = "Invalid payload provided"):
        super().__init__(message)

__all__ = ["AgentNotFoundError", "InvalidPayloadError"]