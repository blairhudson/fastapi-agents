from smolagents.agents import MultiStepAgent, ToolCallingAgent, CodeAgent
from fastapi_agents.models import RequestPayload
from fastapi_agents import logger
import json

class SmolagentsAgent(MultiStepAgent):
    def __init__(self, agent: MultiStepAgent):
        self.agent = agent

    async def run(self, payload: RequestPayload) -> dict:
        validated_payload = RequestPayload(**payload.dict())
        logger.info(f"Validated payload: {validated_payload}")

        # if messages len > 1 and role is not user, return error
        if len(validated_payload.messages) > 1 and not all([message.role == "user" for message in validated_payload.messages]):
            raise ValueError("Only one user message is allowed.")

        result = self.agent.run(validated_payload.messages[0].content)

        if type(self.agent) == ToolCallingAgent:
            return json.loads(result).get("answer", "")
        elif type(self.agent) == CodeAgent:
            return str(result)
        else:
            return str(result)
    