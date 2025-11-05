# writing-agentic-rag# 100% private Agentic RAG API

This is a simple API that uses CrewAI and LitServe to create a 100% private Agentic RAG API.

## How to use

1. Clone the repo
2. Install the dependencies:

```bash
uv add pydantic-ai pyton-dotenv litserve

3. Run the server:

```bash
python server.py
```

4. Run the client:

```bash
python client.py --query "What is the Qwen3?"
```

# Health check
```bash
    curl http://localhost:8000/api/v1/health
``` 

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.