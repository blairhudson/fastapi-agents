FROM python:3.12-slim-bookworm

# Build args
ARG PACKAGE_VERSION=0.1
ARG AGENT_FRAMEWORK

# Environment variables
ENV AGENT_FRAMEWORK=${AGENT_FRAMEWORK}
ENV AGENT_MODULE=agent.pydantic_ai
ENV AGENT_CLASS=agent
ENV SECURITY_MODULE=
ENV SECURITY_CLASS=
ENV API_ENDPOINT=pydanticai
ENV API_PREFIX=/agents
ENV API_MODE=simple

# Create a directory for pip installations
RUN mkdir -p /app/.local && chown nobody:nogroup /app/.local
ENV PYTHONUSERBASE=/app/.local
ENV PATH="$PYTHONUSERBASE/bin:$PATH"

# Configure entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER nobody

# Install dependencies
RUN pip install --user --no-cache-dir "fastapi-agents[${AGENT_FRAMEWORK},uvicorn,security]~=${PACKAGE_VERSION}"

# Prepare the app
WORKDIR /app
COPY --chown=nobody ./main.py /app

# Prepare the default agent, we expect it to be volume mounted at runtime
COPY --chown=nobody ./agent /app/agent

# Run the app
ARG PORT=8080
ENV PORT=${PORT}
EXPOSE ${PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
