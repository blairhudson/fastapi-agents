from fastapi import FastAPI
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

app = FastAPI()

agents = FastAPIAgents(path_prefix="/agents")

agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent))

app.include_router(agents)