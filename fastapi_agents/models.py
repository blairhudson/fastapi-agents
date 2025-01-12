from pydantic import BaseModel
from enum import Enum
from typing import List

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    content: str
    role: Role

class RequestPayload(BaseModel):
    messages: List[Message]

class ResponsePayload(BaseModel):
    message: Message


# Base Agent Class
class BaseAgent:
    async def run(self, payload: RequestPayload) -> dict:
        raise NotImplementedError
