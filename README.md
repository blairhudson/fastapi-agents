# FastAPI Agents

**FastAPI Agents** is the ultimate FastAPI extension for integrating AI agents into your applications. With just a few lines of code, you can create, manage, and secure AI-powered endpoints, enabling you to build smarter, more interactive apps effortlessly. Whether you're a seasoned developer or just exploring AI integrations, FastAPI Agents has you covered! 🎉

## ✨ Features at a Glance

- 🤖 **Easy Agent Management**: Register, organize, and interact with multiple AI agents seamlessly.
- 🔐 **Built-In Security**: Easily add API key, OAuth2, cookie, or OpenID authentication to your endpoints.
- 📚 **Agent Framework Support**: Compatible with agent frameworks like PydanticAI, Llama-Index, and HuggingFace Smolagents.
- 🐳 **Pre-Built Containers**: Easily deploy agents in your favourite framework with ready made containers.
- 🛠️ **Extensibility**: Support additional agent frameworks by extending the `BaseAgent` class.
- 🧩 **Dynamic Dependencies**: Inject and resolve request-specific configurations effortlessly.
- 🚀 **Performance Optimized**: Leverage FastAPI's high performance and scalability for AI agent interactions.
- 📖 **Auto-Generated API Documentation**: OpenAPI integration for your registered agents, out of the box!

## 💖 Sponsors

You can support the ongoing development of FastAPI Agents by becoming a sponsor:

[Sponsor FastAPI Agents](https://github.com/sponsors/blairhudson)

## 📚 Documentation

For further documentation, including detailed API documentation for the available agent frameworks, visit the [FastAPI Agents Documentation](https://fastapi-agents.blairhudson.com/).

## 🚀 Installation

Install `FastAPI Agents` using pip, poetry or uv:

```bash
pip install fastapi-agents
poetry add fastapi-agents
uv add fastapi-agents
```

Install optional extras for your chosen agent frameworks:

```bash
pip install fastapi-agents[pydantic_ai]
poetry add fastapi-agents -E pydantic_ai
uv add fastapi-agents --extra pydantic_ai
```

For available extras, replace `pydantic_ai` with the desired agent framework. See [pyproject.toml](pyproject.toml) for the full list of extras.

That's it! You're all set to start integrating AI agents into your FastAPI applications. 🎉

## 🏁 Quick Start

### Registering Agents

Here’s how to get started with a basic `PydanticAI` agent:

```python
from fastapi import FastAPI
from fastapi_agents import FastAPIAgents
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

app = FastAPI()
agents = FastAPIAgents(path_prefix="/agents")

# Initialize and register the agent
agent = Agent("openai:gpt-4o-mini")
agents.register("pydanticai", PydanticAIAgent(agent))

# Include the router
app.include_router(agents)
```

### Adding Security

Secure your endpoints with API Key authentication in just a few steps:

```python
from fastapi.security import APIKeyHeader
from fastapi_agents import FastAPIAgents

# Define API Key validation
def validate_api_key(api_key: str = Depends(APIKeyHeader(name="X-API-Key"))):
    if api_key != "my-secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Secure the agents
agents = FastAPIAgents(path_prefix="/agents", security_dependency=validate_api_key)
```

👉 See [examples/security_apikey.py](examples/security_apikey.py) for more details.

### Running the Application

Run your FastAPI application with the registered agents:

```bash
uvicorn --reload <module>:app
```

Replace `<module>` with the name of the Python module containing your FastAPI application.

That's it! You're all set to start building smarter, more secure FastAPI applications with AI agents. 🚀

## 🤝 Supported Agents

`FastAPI Agents` supports a variety of agent frameworks, including:

1. **PydanticAI**: AI agents powered by Pydantic AI. [Examples](https://github.com/blairhudson/fastapi-agents/tree/main/examples/pydantic-ai)
2. **Llama Index**: OpenAI agents with Llama Index integration. [Examples](https://github.com/blairhudson/fastapi-agents/tree/main/examples/llama-index)
3. **HuggingFace Smolagents**: Lightweight and efficient AI agents. [Examples](https://github.com/blairhudson/fastapi-agents/tree/main/examples/smolagents)

## ⚙️ Configuration Options

### `FastAPIAgents`

The `FastAPIAgents` class is initialized with the following parameters:

| Parameter              | Type                | Default         | Description                                                                                 |
|------------------------|---------------------|-----------------|---------------------------------------------------------------------------------------------|
| `path_prefix`          | `Optional[str]`    | `"/agents"`     | The prefix for all agent-related endpoints. Can be set to `None` for no prefix.             |
| `security_dependency`  | `Optional[Callable]` | `None`        | A global security dependency for all agents. For example, API key or OAuth validation.      |
| `*args`                | `Any`              | `-`             | Additional arguments passed to the parent `APIRouter` class.                                |
| `**kwargs`             | `Any`              | `-`             | Additional keyword arguments passed to the parent `APIRouter` class.                        |

**Example**:
```python
agents = FastAPIAgents(
    path_prefix="/agents", 
    security_dependency=validate_api_key
)
```

### `FastAPIAgents.register`

The `register` method is used to add an individual agent. The following parameters are available:

| Parameter              | Type                | Required | Default       | Description                                                                                 |
|------------------------|---------------------|----------|---------------|---------------------------------------------------------------------------------------------|
| `name`                 | `str`              | Yes      | -             | The unique name for the agent. This will form part of the endpoint URL.                     |
| `agent`                | `BaseAgent`        | Yes      | -             | An instance of a class that implements the `BaseAgent` interface.                          |
| `router`               | `Optional[APIRouter]` | No   | `None`        | A custom router to include this agent. Defaults to the global `FastAPIAgents` router.       |
| `tags`                 | `Optional[List[str]]` | No   | `["Agents"]`  | Tags to include in the OpenAPI documentation for this agent's endpoints.                   |
| `description`          | `Optional[str]`    | No       | `None`        | A description for the agent's endpoint in the OpenAPI documentation.                       |
| `security_dependency`  | `Optional[Callable]` | No   | `None`        | A per-agent security dependency, overriding the global `security_dependency` if set.        |

> **Note**: A per-agent security dependency cannot be used if a global `security_dependency` is already defined during initialization.

**Example**:
```python
from fastapi_agents.pydantic_ai import PydanticAIAgent
from pydantic_ai import Agent

agent = Agent("openai:gpt-4o-mini")

agents.register(
    name="pydanticai",
    agent=PydanticAIAgent(agent),
    tags=["AI Agents"],
    description="An agent for handling Pydantic AI interactions."
)
```

### Key Behaviors

- **Global Security vs. Per-Agent Security**: 
    - If a `security_dependency` is provided at the `FastAPIAgents` level, it applies to all agents unless overridden by a per-agent `security_dependency`.
    - Defining both global and per-agent security will raise a `ValueError`.

- **Endpoint URLs**:
    - The endpoint for an agent is constructed as `{path_prefix}/{name}`. 
    - If `path_prefix` is `None`, the URL becomes `/{name}`.

## 🐳 Using Docker

### Pre-Built Images

Pre-built Docker images for `FastAPI Agents` are available on GitHub Container Registry (GHCR):

- **Repository**: `ghcr.io/blairhudson/fastapi-agents`
- Tags:
  - Framework-specific: `pydantic-ai`, `smolagents`, `llama-index`
  - Version-specific: `<framework>-<version>`

To pull a specific image:

```bash
docker pull ghcr.io/blairhudson/fastapi-agents:pydantic-ai
```

### Environment Variables

The pre-built images support the following environment variables for customisation:

| Variable           | Example Value      | Description                                                |
|--------------------|--------------------|------------------------------------------------------------|
| `AGENT_FRAMEWORK`  | `pydantic-ai`     | Specifies the agent framework to use.                      |
| `AGENT_MODULE`     | `agent.pydantic_ai` | Path to the agent module.                                  |
| `AGENT_CLASS`      | `agent`           | Class name for the agent.                                  |
| `SECURITY_MODULE`  | `agent.pydantic_ai` | Specifies the security module for the agent. |
| `SECURITY_CLASS` | `validate_token` | Class name for the security depdency. |
| `API_ENDPOINT`     | `pydantic-ai`      | API endpoint path for the agent.                           |
| `API_PREFIX`       | `/agents`         | Prefix for all agent-related API endpoints.                |
| `PORT`             | `8080`            | Port the application runs on within the container.         |

To customize these values, pass them as `-e` arguments to `docker run` or define them in an `.env` file.

### Volume Mounting

Agents are expected to be volume-mounted at `/app/agent`. You can mount your agent directory as follows:

```bash
docker run -p 8000:8080 \
  -v $(pwd)/agent:/app/agent \
  ghcr.io/blairhudson/fastapi-agents:pydantic-ai
```

If a `requirements.txt` file is present in the mounted directory, it will be automatically installed at container startup.

### Building Custom Containers

For production deployments, it is recommended to build your container with dependencies included. Here’s an example `Dockerfile` starting from one of the pre-built base images:

```dockerfile
FROM ghcr.io/blairhudson/fastapi-agents:pydantic-ai

# Copy your agent source code
COPY ./agent /app/agent

# Install dependencies
RUN pip install --no-cache-dir -r /app/agent/requirements.txt
```

Build and run the custom image:

```bash
docker build -t my-custom-agent .
docker run -p 8000:8080 my-custom-agent
```

This approach ensures all dependencies are baked into the image, improving startup performance and reliability.

## 💡 Examples

Explore real-world examples for implementing `FastAPI Agents` in different scenarios:

- **Agent Frameworks**:
    - [PydanticAI](https://github.com/blairhudson/fastapi-agents/tree/main/examples/pydantic-ai/pydantic_ai.py)
    - [Llama-Index](https://github.com/blairhudson/fastapi-agents/tree/main/examples/llama-index/llama_index.py)
    - [Huggingface SmolAgents](https://github.com/blairhudson/fastapi-agents/tree/main/examples/smolagents/smolagents.py)
- **Advanced Agent Frameworks**:
    - [PydanticAI with Dependencies](https://github.com/blairhudson/fastapi-agents/tree/main/examples/pydantic-ai/pydantic_ai_deps.py)
- **Docker*:
    - [PydanticAI in Docker](https://github.com/blairhudson/fastapi-agents/tree/main/examples/docker)
- **Security Integrations**:
    - [API Key Authentication](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security/security_apikey.py)
    - [Cookie Authentication](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security/security_cookie.py)
    - [OAuth2 Authentication](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security/security_oauth2.py)
    - [OpenID Connect (OIDC)](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security/security_oidc.py)
    - [HTTP Basic Auth](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security/security_httpbasic.py)

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Add any new tests and ensure they pass. i.e. `uv run pytest`.
4. Submit a pull request.

For any questions or feature requests including additional agent frameworks, open an issue in the repository.

## 📄 Citation

If you use **FastAPI Agents** in your work, please consider citing it using the metadata in the `CITATION.cff` file:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14635504.svg)](https://doi.org/10.5281/zenodo.14635504)

This DOI represents all versions of the project. For version-specific DOIs, refer to the [Zenodo project page](https://doi.org/10.5281/zenodo.14635504).

Alternatively, you can use the following BibTeX entry:

```bibtex
@software{fastapi_agents,
  author = {Blair Hudson},
  title = {FastAPI Agents},
  year = {2025},
  version = {0.1},
  doi = {10.5281/zenodo.14635504},
  url = {https://github.com/blairhudson/fastapi-agents},
  orcid = {https://orcid.org/0009-0007-4216-4555},
  abstract = {FastAPI Agents is the ultimate FastAPI extension for integrating AI agents into your applications.}
}
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
