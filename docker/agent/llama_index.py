from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

agent = OpenAIAgent.from_llm(tools=None, llm=OpenAI("gpt-4o-mini"))
