from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Dict, Optional, List

import logging

from fastapi_agents.models import BaseAgent, RequestPayload, ResponsePayload
from fastapi_agents.errors import AgentNotFoundError

# Logging setup
logger = logging.getLogger("fastapi_agents")
logging.basicConfig(level=logging.INFO)


class FastAPIAgents(APIRouter):
    def __init__(
        self,
        path_prefix: Optional[str] = "/agents",
        security_dependency: Optional[Callable] = None,  # Global security dependency
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.agents: Dict[str, BaseAgent] = {}
        self.path_prefix = path_prefix.rstrip("/") if path_prefix else ""
        self.global_security_dependency = security_dependency  # Store global security

    def register(
        self,
        name: str,
        agent: BaseAgent,
        router: Optional[APIRouter] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        security_dependency: Optional[Callable] = None,  # Optional per-agent security
    ):
        # Error if attempting to override global security
        if self.global_security_dependency and security_dependency:
            raise ValueError(
                f"Cannot set a per-agent security dependency for '{name}' "
                "because a global security dependency is already defined."
            )

        self.agents[name] = agent
        target_router = router or self
        route_path = f"{self.path_prefix}/{name}" if self.path_prefix else f"/{name}"

        # Use global security if no per-agent security is defined
        effective_security = security_dependency or self.global_security_dependency

        if effective_security:
            # Endpoint with security
            @target_router.post(route_path, tags=tags or ["Agents"], description=description)
            async def agent_endpoint(
                payload: RequestPayload,
                token: str = Depends(effective_security),  # Extract token via security dependency
                agent: BaseAgent = Depends(self._get_agent(name)),
            ) -> ResponsePayload:
                try:
                    # Log the token for debugging
                    logger.info(f"Token received for agent '{name}': {token}")

                    # Process the agent logic
                    result = await agent.run(payload)
                    return JSONResponse({"message": {"role": "assistant", "content": result}})
                except Exception as e:
                    logger.error(f"Error in endpoint for agent '{name}': {e}")
                    raise HTTPException(status_code=500, detail=str(e))
        else:
            # Endpoint without security
            @target_router.post(route_path, tags=tags or ["Agents"], description=description)
            async def agent_endpoint(
                payload: RequestPayload,
                agent: BaseAgent = Depends(self._get_agent(name)),
            ) -> ResponsePayload:
                try:
                    # Process the agent logic
                    result = await agent.run(payload)
                    return JSONResponse({"message": {"role": "assistant", "content": result}})
                except Exception as e:
                    logger.error(f"Error in endpoint for agent '{name}': {e}")
                    raise HTTPException(status_code=500, detail=str(e))

    def _get_agent(self, name: str) -> Callable[[], BaseAgent]:
        def _get_agent_instance():
            agent = self.agents.get(name)
            if not agent:
                raise AgentNotFoundError(name)
            return agent

        return _get_agent_instance
