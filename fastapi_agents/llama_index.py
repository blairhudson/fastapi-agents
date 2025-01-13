from typing import Any, Callable, List
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.base.llms.types import ChatMessage

from fastapi_agents.models import RequestPayload

from fastapi_agents import logger

class LlamaIndexAgent(AgentRunner):
    """
    Adapter class to wrap a LlamaIndex agent for use with FastAPIAgents.

    Parameters:
        agent (Callable[[AgentRunner], Any]): The LlamaIndex agent.

    Example:
    
        from fastapi_agents.llama_index import LlamaIndexAgent
        from llama_index.agent.openai import OpenAIAgent
        from llama_index.llms.openai import OpenAI

        agent = OpenAIAgent.from_llm(tools=None, llm=OpenAI("gpt-4o-mini"))
        agents.register("llamaindex", LlamaIndexAgent(agent))

    Raises:
        ValueError: If the agent is not a LlamaIndex agent.
        
    Returns:
        LlamaIndexAgent: A LlamaIndex agent.

    """
    def __init__(self, agent: Callable[[AgentRunner], Any]):
        self.agent = agent

        if not isinstance(agent, AgentRunner):
            raise ValueError("Agent is not a LlamaIndex agent.")

    async def run(self, payload: RequestPayload) -> dict:
        validated_payload = RequestPayload(**payload.dict())
        logger.info(f"Validated payload: {validated_payload}")

        # get last content from payload messages where role is user
        chat_message = [message for message in validated_payload.messages if message.role == "user"][-1]
        
        chat_history = convert_messages_to_llamaindex({"messages": validated_payload.messages})
        
        response = await self.agent.achat(chat_message.content, chat_history=chat_history)
        return response.response
    
def convert_messages_to_llamaindex(messages: dict) -> List[ChatMessage]:
    """Converts messages e.g. {"messages": [{"role":"role","content":"content"}]} to LlamaIndex ChatMessage objects."""
    return [ChatMessage(content=message.content, role=message.role) for message in messages["messages"]]
