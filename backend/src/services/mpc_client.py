from fastmcp import Client


def get_mcp_client() -> Client:
    return Client("http://localhost:8000/api/llm/mcp")
