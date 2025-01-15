from smolagents import LiteLLMModel
from smolagents import ToolCallingAgent

model = LiteLLMModel("gpt-4o-mini")
agent = ToolCallingAgent(tools=[], model=model)