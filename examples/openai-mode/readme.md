# FastAPI Agents PydanticAI Docker Example with OpenAI Mode

To run this example, run `docker compose up`. Ensure your `OPENAI_API_KEY` is set in the appropriate `.env` file or passed as an additional environment variable.

You will be able to create a chat completion using your agent at `http://localhost:8080/chat/completions` and see your agent as an available model at `http://localhost:8080/models` using the header `Authorization: Bearer <token>` (`valid_token` by default).

You can access the FastAPI docs at `http://localhost:8080/docs`.