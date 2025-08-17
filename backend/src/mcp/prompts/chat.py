from fastmcp import FastMCP


def register_chat_prompts(mcp: FastMCP):
    @mcp.prompt
    def hello_prompt():
        """Generates a user message for retrieving all contacts"""
        return "Hello! Please introduce yourself according to your system prompt."
