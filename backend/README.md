# Backend

## Development

To run the app, in `backend` directory run:

```bash
uv sync

source ./.venv/bin/activate

uv run fastapi dev src/main.py
```

To run MCP inspector (make sure the backend is running first):

```bash
npx @modelcontextprotocol/inspector
```

In the inspector UI:

- **Transport Type**: `Streamable HTTP`
- **URL**: `http://localhost:8000/api/llm/mcp`

Then click **Connect**.
