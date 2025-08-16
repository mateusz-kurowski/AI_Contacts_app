# src/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat import router as chat_router
from src.api.contacts import router as contacts_router
from fastmcp import FastMCP

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
mcp = FastMCP.from_fastapi(base_app)
mcp_app = mcp.http_app(path="/mcp")

app = create_base_app(lifespan=mcp_app.lifespan)
app.mount("/llm", mcp_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
