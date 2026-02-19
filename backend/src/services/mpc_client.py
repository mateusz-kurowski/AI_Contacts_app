from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


def get_mcp_client() -> Client:
    return Client(StreamableHttpTransport("http://localhost:8000/api/llm/mcp"))
