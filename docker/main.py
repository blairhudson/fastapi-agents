from fastapi import FastAPI
from fastapi_agents import FastAPIAgents
import os
import importlib

# get environment variables
agent_framework = os.getenv("AGENT_FRAMEWORK", "pydantic_ai")
agent_module = os.getenv("AGENT_MODULE", "agent")
agent_class = os.getenv("AGENT_CLASS", "agent")
security_module = os.getenv("SECURITY_MODULE", None)
security_class = os.getenv("SECURITY_CLASS", None)
api_endpoint = os.getenv("API_ENDPOINT", "pydanticai")
api_prefix = os.getenv("API_PREFIX", "/agents")
api_mode = os.getenv("API_MODE", "simple")

if security_module == '':
    security_module = None

if security_class == '':
    security_class = None

# dynamically import agent framework
if agent_framework == "pydantic-ai":
    from fastapi_agents.pydantic_ai import PydanticAIAgent as AgentWrapper
    from pydantic_ai import Agent as BaseAgentClass
elif agent_framework == "smolagents":
    from fastapi_agents.smolagents import SmolagentsAgent as AgentWrapper
    from smolagents import MultiStepAgent as BaseAgentClass
elif agent_framework == "llama-index":
    from fastapi_agents.llama_index import LlamaIndexAgent as AgentWrapper
    from llama_index.core.agent.types import BaseAgent as BaseAgentClass
else:
    raise ValueError(f"Unknown agent framework: {agent_framework}")

# create FastAPI app and FastAPIAgents instance
app = FastAPI()
agents = FastAPIAgents(path_prefix=api_prefix, mode=api_mode)

# dynamically import agent module
import_agent_module = importlib.import_module(agent_module)
agent = getattr(import_agent_module, agent_class)

# check type of agent
if not issubclass(type(agent), BaseAgentClass):
    raise ValueError(f"Agent must be a subclass of {type(BaseAgentClass)}, not {agent}")

# dynamically import security module
if security_class and security_module:
    import_security_module = importlib.import_module(security_module)
    security = getattr(import_security_module, security_class)
elif security_class or security_module:
    raise ValueError("Both SECURITY_MODULE and SECURITY_CLASS must be set to enable security.")
else:
    security = None

# register agent with FastAPIAgents
agents.register(
    api_endpoint, 
    AgentWrapper(agent), 
    security_dependency=security
)
app.include_router(agents)
