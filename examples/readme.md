# FastAPI Agents Examples

You can run most examples with `uvicorn`. 

Run `uvicorn --reload <module>:app` from the example directory, replacing `<module>` with the Python filename without the extension.

For example:

```
cd pydantic-ai
pip install uvicorn fastapi fastapi-agents pydantic-ai
uvicorn --reload pydantic_ai:app
```

## List of Examples

- **Notebooks**:
  - FastAPI Agents Step-by-Step.ipynb - A step-by-step walkthrough of configuring FastAPI Agents with PydanticAI including tool definitions to build a demo todo list manager agent and serve as an API. Runs within a Jupyter notebook so you can execute each part in sequence to see what happens. Not recommended for production.
- **PydanticAI:**
  - pydantic_ai - A basic example showing how to use a PydanticAI agent with FastAPI Agents
  - pydantic_ai_deps - Adding depdendency injection to PydanticAI
- **Llama-Index:**
  - llama_index - A basic example showing how to use a Llama-Index agent with FastAPI Agents
- **Smolagents:**
  - smolagents - A basic example showing how to use a smolagents agent with FastAPI Agents
- **Security:**
  - security_apikey - Adding FastAPI security dependency with API Key header authentication
  - security_cookie - Adding FastAPI security dependency with cookie-based authentication
  - security_httpbasic - Adding FastAPI security dependency with HTTP Basic (username/password) authentication
  - security_oauth2 - Adding FastAPI security dependency with Oauth2 (Bearer) authentication
  - security_oidc - Adding FastAPI security dependency with OIDC-based authentication
- **Docker:**
  - PydanticAI with OAuth2 security using fastapi-agents container
