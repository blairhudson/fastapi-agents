from fastapi import FastAPI
from fastapi_agents import FastAPIAgents
from fastapi_agents.llama_index import LlamaIndexAgent
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

app = FastAPI()

agents = FastAPIAgents(path_prefix="/agents")

agent = OpenAIAgent.from_llm(tools=None, llm=OpenAI("gpt-4o-mini"))
agents.register("llamaindex", LlamaIndexAgent(agent))

app.include_router(agents)