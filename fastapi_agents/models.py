from abc import ABC, abstractmethod
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class Role(str, Enum):
    """
    Role of the message in the conversation.

    Values:
        - `user`: Messages sent by the user.
        - `assistant`: Messages sent by the agent.
    """
    USER = "user"
    ASSISTANT = "assistant"

class APIMode(str, Enum):
    """
    Mode for registering routes to FastAPI.

    Values:
        - `simple`: Standard mode with minimal configuration.
        - `openai`: OpenAI-compatible mode for additional functionality.
    """
    
    SIMPLE = "simple"
    OPENAI = "openai"

class Message(BaseModel):
    """
    Message object in the conversation.
    
    Args:
        content (str): The content of the message.
        role (Role): The role of the message in the conversation.
        
    Returns:
        Message: An instance of the Message object.
    """
    content: str
    role: Role

class RequestPayload(BaseModel):
    """
    Request payload for the agent endpoint.
    
    Args:
        messages (List[Message]): A list of messages in the conversation.
        
    Returns:
        RequestPayload: An instance of the RequestPayload object.
    """
    messages: List[Message]

class ResponsePayload(BaseModel):
    """
    Response payload for the agent endpoint.

    Args:
        message (Message): The message to return in the response.

    Returns:
        ResponsePayload: An instance of the ResponsePayload object.
    """
    message: Message

class OpenAIRequestPayload(BaseModel):
    model: str
    messages: List[Message]

class Choice(BaseModel):
    index: int
    message: Optional[Message]
    finish_reason: Optional[str]

class OpenAIResponsePayload(BaseModel):
    id: str = "chatcmpl-123"
    object: str = "chat.completion"
    model: str
    created: int
    choices: List[Choice]

# Base Agent Class, can't be instantiated, decorate as such

class BaseAgent(ABC):
    """
    Base class for an agent.
    """
    @abstractmethod
    async def run(self, payload: RequestPayload) -> dict:
        """
        Run the agent with the given payload.
        
        Args:
            payload (RequestPayload): The payload for the agent.
            
        Returns:
            dict: The response from the agent.
        """
        raise NotImplementedError

__all__ = ["Role", "APIMode", "Message", "RequestPayload", "ResponsePayload", "OpenAIRequestPayload", "OpenAIResponsePayload", "BaseAgent"]