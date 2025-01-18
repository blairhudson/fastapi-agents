# FastAPI Agents Roadmap

## Agent Framework support

- [x] Pydantic AI
  - [ ] Pydantic Graph
- [x] Llama-Index
- [x] Smolagents
- [ ] CrewAI
- [ ] LangChain
  - [ ] LangGraph
- [ ] Autogen

## API Features

- [x] Simple mode (one endpoint per agent)
- [x] Customisable security dependencies
  - [x] Per agent security
- [x] OpenAI mode
  - [x] Chat Completions endpoint
  - [x] Models endpoint
- [ ] Streaming
- [ ] Output tool selection ("inner thoughts")
- [ ] Increased request concurrency

## Containers

- [x] Pre-built Containers for each Agent framework
- [x] Dynamic requirements.txt
- [ ] Support for Multiple Agents in one container
- [ ] Alternative package manager support
  - [ ] Poetry
  - [ ] UV
- [ ] Reduce container sizes

## Developer experience

- [x] Standalone doc site
- [x] Examples folder
  - [ ] Examples on doc site
- [x] Guided notebooks
- [x] Flexible router attachment
- [x] Optional FastAPI app creation  
- [ ] Automatic framework adapter selection
- [ ] Gradio UI

## Contributor experience

- [x] Automated tests
- [ ] Code coverage reporting
- [ ] Issue templates