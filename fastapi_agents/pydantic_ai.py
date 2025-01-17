from datetime import datetime
from types import NoneType
from typing import Any, Callable, Optional
from fastapi_agents.models import RequestPayload, BaseAgent
from fastapi_agents.logs import logger
from pydantic_ai import Agent
from pydantic_ai.messages import ModelRequest, UserPromptPart
from fastapi_agents.errors import InvalidPayloadError


from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart
)

def convert_messages_to_pydanticai(data: dict):
    messages = data.get("messages", [])
    conversation = []
    partial_request = None

    for msg in messages:
        role = getattr(msg, "role", None)
        content = getattr(msg, "content", "")

        if role == "system":
            if partial_request is None:
                partial_request = ModelRequest(parts=[], kind="request")
            partial_request.parts.append(
                SystemPromptPart(
                    content=content,
                    part_kind="system-prompt",
                    dynamic_ref=None
                )
            )

        elif role == "user":
            if partial_request is None:
                partial_request = ModelRequest(parts=[], kind="request")
            partial_request.parts.append(
                UserPromptPart(
                    content=content,
                    timestamp=datetime.now(),
                    part_kind="user-prompt"
                )
            )
            conversation.append(partial_request)
            partial_request = None

        elif role == "assistant":
            if partial_request is not None:
                conversation.append(partial_request)
                partial_request = None

            conversation.append(
                ModelResponse(
                    parts=[
                        TextPart(
                            content=content,
                            part_kind="text"
                        )
                    ],
                    timestamp=datetime.now(),
                    kind="response"
                )
            )

    if partial_request is not None:
        conversation.append(partial_request)

    return conversation


class PydanticAIAgent(BaseAgent):
    """
    Adapter class to wrap a Pydantic AI Agent for use with FastAPIAgents and resolve runtime dependencies.
    
    Parameters:
        agent (Agent): The Pydantic AI Agent with `deps_type` specified.
        deps (Optional[Callable[[], Any]]): Optional function to resolve runtime dependencies.
    
    Example:

        from fastapi_agents.pydantic_ai import PydanticAIAgent
        from pydantic_ai import Agent

        agent = Agent("openai:gpt-4o-mini")
        pydantic_ai_agent = PydanticAIAgent(agent)

    Raises:
        ValueError: If the agent has `deps_type` specified, but `deps` resolver is not provided.
        ValueError: If the agent does not have `deps_type` specified, but `deps` resolver is provided.
        
    Returns:
        PydanticAIAgent: A Pydantic AI Agent with runtime dependency resolution.
    """
    def __init__(
        self,
        agent: Agent,  # The Pydantic AI Agent with deps_type
        deps: Optional[Callable[[], Any]] = None,  # Optional function to resolve runtime dependencies
    ):
        self.agent = agent
        
        if self.agent._deps_type is not NoneType and not deps:
            raise ValueError(
                "Agent has `deps_type` specified, but `deps` resolver is not provided."
            )
        if not self.agent._deps_type and deps:
            raise ValueError(
                "Agent does not have `deps_type` specified, but `deps` resolver is provided."
            )
        self.deps = deps

    async def run(self, payload: RequestPayload) -> dict:
        try:
            # Validate and parse the payload
            logger.info(f"Payload received: {payload}")
            message_history = convert_messages_to_pydanticai({"messages": payload.messages})

            # Extract the user prompt
            user_prompt_message = next(
                (
                    msg.parts[0].content
                    for msg in reversed(message_history)
                    if isinstance(msg, ModelRequest) and any(
                        isinstance(part, UserPromptPart) for part in msg.parts
                    )
                ),
                None,
            )
            if not user_prompt_message:
                raise InvalidPayloadError("No user prompt found in the provided messages.")

            # Resolve runtime dependencies if `deps` is provided
            validated_deps = None
            if self.deps:
                deps_values = await self.deps()
                if self.agent._deps_type:
                    validated_deps = self.agent._deps_type(**deps_values)

            # Prepare arguments for the agent
            kwargs = {
                "user_prompt": user_prompt_message,
                "message_history": message_history[:-1],  # Exclude the last message
            }
            if validated_deps:
                kwargs["deps"] = validated_deps

            # Call the underlying agent
            response = await self.agent.run(**kwargs)

            return response.data if hasattr(response, "data") else ""

        except Exception as e:
            logger.error(f"Error in PydanticAIAgent: {e}")
            raise

__all__ = ["PydanticAIAgent"]