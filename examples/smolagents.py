from fastapi import FastAPI
from fastapi_agents import FastAPIAgents
from fastapi_agents.smolagents import SmolagentsAgent
from smolagents import LiteLLMModel
from smolagents import ToolCallingAgent

app = FastAPI()

agents = FastAPIAgents(path_prefix="/agents")

model = LiteLLMModel("gpt-4o-mini")
agent = ToolCallingAgent(tools=[], model=model)

agents.register("smolagents", SmolagentsAgent(agent))

app.include_router(agents)