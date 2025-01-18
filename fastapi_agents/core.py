import time, os
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Any, Callable, Dict, Optional, List
import warnings
from fastapi_agents.logs import logger
from fastapi_agents.models import BaseAgent, OpenAIRequestPayload, OpenAIResponsePayload, RequestPayload, ResponsePayload, APIMode, Message, Choice
from fastapi_agents.errors import AgentNotFoundError

class FastAPIAgents(APIRouter):
    """
    FastAPI router for managing multiple agents.

    This router is designed to be used with FastAPI to manage multiple agents, each with its own endpoint.

    Args:
        path_prefix (str, optional): The path prefix for the agents' endpoints. Defaults to "/agents".
        security_dependency (Callable, optional): A global security dependency for all agents. Defaults to None.
        mode (APIMode, optional): The mode for registering routes. Defaults to "simple". Also available is "openai" which registers routes as OpenAI-compatible.
        *args (list[Any], optional): Additional arguments to pass to the APIRouter parent class.
        **kwargs (dict[str, Any], optional): Additional keyword arguments to pass to the APIRouter parent class.
    
    Raises:
        ValueError: If a per-agent security dependency is defined when a global security dependency is already set.
    
    Example:
        
        from fastapi import FastAPI, Depends, HTTPException
        from fastapi_agents import FastAPIAgents
        from fastapi_agents.pydantic_ai import PydanticAIAgent
        from pydantic_ai import Agent

        # Initialize FastAPI app
        app = FastAPI()

        # Initialize FastAPIAgents
        agents = FastAPIAgents(path_prefix="/agents")

        # Register PydanticAI agent
        agent = Agent("openai:gpt-4o-mini")
        agents.register("pydanticai", PydanticAIAgent(agent), tags=["AI Agents"], description="Pydantic AI Agent")

        # Include the router
        app.include_router(agents)
        
    Returns:
        FastAPIAgents (FastAPIAgents): A FastAPI router for managing multiple agents.
        
    """
    def __init__(
        self,
        path_prefix: Optional[str] = None,
        security_dependency: Optional[Callable] = None,  # Global security dependency
        mode: Optional[APIMode] = 'simple',
        *args: Optional[list[Any]],
        **kwargs: Optional[dict[str, Any]]
    ):
        super().__init__(*args, **kwargs)

        # default is '/agents' only if mode is simple
        if mode == 'simple' and path_prefix is None:
            path_prefix = '/agents'

        if path_prefix == '/':
            path_prefix == ''

        # make sure mode is one of APIMode str enum
        if mode not in APIMode._value2member_map_:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {list(APIMode._value2member_map_.keys())}")        
        self.mode = mode

        self.agents: Dict[str, BaseAgent] = {}
        self.path_prefix = path_prefix.rstrip("/") if path_prefix else ""
        self.global_security_dependency = security_dependency  # Store global security


    @classmethod
    def as_app(cls, 
               path_prefix: Optional[str] = None,
        security_dependency: Optional[Callable] = None,  # Global security dependency
        mode: Optional[APIMode] = 'simple',
        *args: Optional[list[Any]],
        **kwargs: Optional[dict[str, Any]]) -> FastAPI:
        """
        Creates and returns a FastAPI app with the FastAPIAgents router included, and injects the `register` method for easy registration.

        Args:
            path_prefix (str, optional): The path prefix for the agents' endpoints. Defaults to "/agents".
            security_dependency (Callable, optional): A global security dependency for all agents. Defaults to None.
            mode (APIMode, optional): The mode for registering routes. Defaults to "simple". Also available is "openai" which registers routes as OpenAI-compatible.
            *args (list[Any], optional): Additional arguments to pass to the APIRouter parent class.
            **kwargs (dict[str, Any], optional): Additional keyword arguments to pass to the APIRouter parent class.
        
        Returns:
            FastAPI: A FastAPI app instance with the router included and registration capability.
        """
        # Initialize the FastAPIAgents instance
        agents_router = cls(path_prefix, security_dependency, mode, *args, **kwargs)

        # Create a FastAPI app
        app = FastAPI()

        # Include the router in the FastAPI app
        app.include_router(agents_router)

        # Add a generic register method to the app
        def register(*register_args, **register_kwargs):
            agents_router.register(*register_args, **register_kwargs)
            app.include_router(agents_router)

        app.register = register  # Attach the register method to the app

        return app

    def register(
        self,
        name: str,
        agent: BaseAgent,
        router: Optional[APIRouter] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        security_dependency: Optional[Callable] = None,  # Optional per-agent security
    ):
        """
        Register an agent with the FastAPI router.

        Args:
            name (str): The name of the agent.
            agent (BaseAgent): The agent instance to register.
            router (APIRouter, optional): The router to use for the agent endpoint. Defaults to None.
            tags (List[str], optional): The tags to assign to the agent endpoint. Defaults to None.
            description (str, optional): The description of the agent endpoint. Defaults to None.
            security_dependency (Callable, optional): A per-agent security dependency. Defaults to None.

        Raises:
            ValueError: If a per-agent security dependency is defined when a global security dependency is already set.
            AgentNotFoundError: If the agent is not found in the registry.
        """
        # Error if attempting to override global security
        if self.global_security_dependency and security_dependency:
            raise ValueError(
                f"Cannot set a per-agent security dependency for '{name}' "
                "because a global security dependency is already defined."
            )

        if name in self.agents.keys():
            raise ValueError(f"Agent '{name}' is already registered.")
        
        if not issubclass(type(agent), BaseAgent):
            raise TypeError(f"Provided agent is not a subclass of BaseAgent. Did you use an adapter?")
        self.agents[name] = agent

        target_router = router or self
        
        if self.mode == "simple":

            # Use global security if no per-agent security is defined
            effective_security = security_dependency or self.global_security_dependency

            route_path = f"{self.path_prefix}/{name}" if self.path_prefix else f"/{name}"

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
                    
        elif self.mode == "openai":

            if tags:
                warnings.warn("Tags provided in openai mode are not used.")

            if description:
                warnings.warn("Descriptions provided in openai mode are not used.")

            if security_dependency:
                raise ValueError(f"Security dependency can only be provided globally in openai mode.") 

            existing_routes = {(route.path, frozenset(route.methods)) for route in target_router.routes}
            
            models_path = f"{self.path_prefix}/models" if self.path_prefix else f"/models"

            if (models_path, frozenset({'GET'})) not in existing_routes:

                if self.global_security_dependency:
                    @target_router.get(models_path, tags=['Models'], description="List and describe the various models available in the API.")
                    async def list_models(token: str = Depends(self.global_security_dependency)) -> JSONResponse:
                        return JSONResponse({
                            "object": "list",
                            "data": [{"id": key, "object": "model", "created": int(os.path.getmtime(__file__)), "owned_by": "openai"} for key in self.agents.keys()]
                        })
                else:
                    @target_router.get(models_path, tags=['Models'], description="List and describe the various models available in the API.")
                    async def list_models() -> JSONResponse:
                        return JSONResponse({
                            "object": "list",
                            "data": [{"id": key, "object": "model", "created": int(os.path.getmtime(__file__)), "owned_by": "openai"} for key in self.agents.keys()]
                        })
                    
            chat_completions_path = f"{self.path_prefix}/chat/completions" if self.path_prefix else f"/chat/completions"
            
            if (chat_completions_path, frozenset({'POST'})) not in existing_routes:
                if self.global_security_dependency:
                    @target_router.post(chat_completions_path, tags=["Chat"], description="Given a list of messages comprising a conversation, the model will return a response.")
                    async def chat_completion(payload: OpenAIRequestPayload, token: str = Depends(self.global_security_dependency)) -> OpenAIResponsePayload:
                        validated_payload = OpenAIRequestPayload.model_validate(payload)
                        name = validated_payload.model

                        try:
                            agent = self._get_agent(name)()
                            result = await agent.run(validated_payload)
                            return OpenAIResponsePayload(
                                id="chatcmpl-123",
                                object="chat.completion",
                                model=name,
                                created=int(time.time()),
                                choices=[Choice(index=0,
                                    message=Message(role="assistant", content=result),
                                    finish_reason="stop"
                                )]
                            ).model_dump()
                        
                        except Exception as e:
                            logger.error(f"Error in endpoint for agent '{name}': {e}")
                            raise HTTPException(status_code=500, detail=str(e))

                else:
                    @target_router.post(chat_completions_path, tags=["Chat"], description="Given a list of messages comprising a conversation, the model will return a response.")
                    async def chat_completion(payload: OpenAIRequestPayload) -> OpenAIResponsePayload:
                        validated_payload = OpenAIRequestPayload.model_validate(payload)
                        name = validated_payload.model

                        try:
                            agent = self._get_agent(name)()
                            result = await agent.run(validated_payload)
                            return OpenAIResponsePayload(
                                id="chatcmpl-123",
                                object="chat.completion",
                                model=name,
                                created=int(time.time()),
                                choices=[Choice(index=0,
                                    message=Message(role="assistant", content=result),
                                    finish_reason="stop"
                                )]
                            ).model_dump()
                        
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

__all__ = ["FastAPIAgents"]