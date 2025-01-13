from abc import ABC, abstractmethod
from pydantic import BaseModel
from enum import Enum
from typing import List

class Role(str, Enum):
    """
    Role of the message in the conversation.

    Args:
        str: The string representation of the role.

    Returns:
        Role: An instance of the Role enum.
    """
    USER = "user"
    ASSISTANT = "assistant"

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
