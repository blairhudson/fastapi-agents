# FastAPI Agents PydanticAI Docker Example

To run this example, run `docker compose up`. Ensure your `OPENAI_API_KEY` is set in the appropriate `.env` file or passed as an additional environment variable.

You will be able to access your agent endpoint at `http://localhost:8080/agent/pydantic-ai` using the header `Authorization: Bearer <token>` (`valid_token` by default).

You can access the FastAPI docs at `http://localhost:8080/docs`.