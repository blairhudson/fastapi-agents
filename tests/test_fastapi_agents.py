import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_agents import FastAPIAgents
from fastapi_agents.models import RequestPayload, BaseAgent
from unittest.mock import AsyncMock

class MockAgent(BaseAgent):
    async def run(self, payload: RequestPayload) -> dict:
        return "Mock Response"

def mock_security_dependency():
    return "mock-token"

@pytest.fixture
def app():
    app = FastAPI()
    agents_router = FastAPIAgents()
    app.include_router(agents_router)
    return app

@pytest.fixture
def test_client(app):
    return TestClient(app)

@pytest.fixture
def mock_agent():
    agent = MockAgent()
    agent.run = AsyncMock(return_value="Mock Response")
    return agent

@pytest.mark.parametrize("agent_name, security_dependency", [
    ("test_agent", None),
    ("secured_agent", mock_security_dependency)
])
def test_register_agent_success(app, test_client, mock_agent, agent_name, security_dependency):
    agents_router = FastAPIAgents(security_dependency=security_dependency)
    agents_router.register(name=agent_name, agent=mock_agent)
    app.include_router(agents_router)

    payload = {"messages": [{"content": "Hello", "role": "user"}]}
    response = test_client.post(f"/agents/{agent_name}", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": {"content": "Mock Response", "role": "assistant"}}
    mock_agent.run.assert_awaited_once_with(RequestPayload(messages=payload["messages"]))

def test_agent_invalid_payload(app, test_client, mock_agent):
    agents_router = FastAPIAgents()
    agents_router.register(name="test_agent", agent=mock_agent)
    app.include_router(agents_router)

    invalid_payload = {"invalid_field": "data"}
    response = test_client.post("/agents/test_agent", json=invalid_payload)

    assert response.status_code == 422  # Unprocessable Entity

def test_agent_not_found(app, test_client):
    agents_router = FastAPIAgents()
    app.include_router(agents_router)

    payload = {"messages": [{"content": "Hello", "role": "user"}]}
    response = test_client.post("/agents/nonexistent_agent", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

def test_register_agent_with_conflicting_security(app, mock_agent):
    agents_router = FastAPIAgents(security_dependency=mock_security_dependency)

    with pytest.raises(ValueError):
        agents_router.register(
            name="conflicting_agent",
            agent=mock_agent,
            security_dependency=lambda: "conflicting-token",
        )

def test_agent_error_handling(app, test_client):
    class FailingAgent(BaseAgent):
        async def run(self, payload: RequestPayload) -> dict:
            raise Exception("Intentional Failure")

    agents_router = FastAPIAgents()
    failing_agent = FailingAgent()
    agents_router.register(name="failing_agent", agent=failing_agent)
    app.include_router(agents_router)

    payload = {"messages": [{"content": "Hello", "role": "user"}]}
    response = test_client.post("/agents/failing_agent", json=payload)

    assert response.status_code == 500
    assert response.json() == {"detail": "Intentional Failure"}

def test_agent_concurrent_requests(app, test_client, mock_agent):
    agents_router = FastAPIAgents()
    agents_router.register(name="test_agent", agent=mock_agent)
    app.include_router(agents_router)

    payload = {"messages": [{"content": "Hello", "role": "user"}]}
    responses = [test_client.post("/agents/test_agent", json=payload) for _ in range(10)]

    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"message": {"content": "Mock Response", "role": "assistant"}}
