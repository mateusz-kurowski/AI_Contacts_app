# src/main.py
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from src.api.chat import router as chat_router
from src.api.contacts import router as contacts_router
from src.mcp.prompts.chat import register_chat_prompts
from src.mcp.prompts.contact import register_contacts_prompts
from src.mcp.tools.contact import register_contact_tools


def create_base_app(lifespan=None) -> FastAPI:
    """Create and configure the base FastAPI app"""
    app = FastAPI(
        title="Contacts API",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.openapi_version = "3.0.2"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(contacts_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")

    @app.get("/api/health")
    def health_check():
        return {"status": "healthy"}

    return app


base_app = create_base_app()

mcp = FastMCP(
    name="Contacts Server",
    instructions="""
    This server provides data about contacts.
    You can use it to retrieve, create, update, and delete contacts.
    """,
    on_duplicate="error",
)

register_contact_tools(mcp)
register_contacts_prompts(mcp)
register_chat_prompts(mcp)
mcp_app = mcp.http_app(path="/mcp", transport="streamable-http")


app = create_base_app(lifespan=mcp_app.lifespan)
app.mount("/api/llm", mcp_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
