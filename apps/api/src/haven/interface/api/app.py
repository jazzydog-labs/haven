"""FastAPI application setup."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter

from haven.config import get_settings
from haven.domain.exceptions import DomainError, RecordNotFoundError
from haven.infrastructure.database.factory import db_factory
from haven.interface.api.commit_routes import router as commit_router
from haven.interface.api.diff_routes import router as diff_router
from haven.interface.api.routes import router as api_router
from haven.interface.api.ttr_routes import router as ttr_router
from haven.interface.graphql.schema import schema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    # Startup
    settings = get_settings()
    app.state.settings = settings

    yield

    # Shutdown
    await db_factory.dispose()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Haven API",
        description="Self-contained microservice with REST and GraphQL APIs",
        version=settings.app.version,
        lifespan=lifespan,
        debug=settings.app.debug,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(diff_router, prefix="/api/v1")
    app.include_router(ttr_router)
    app.include_router(commit_router)

    # Add GraphQL endpoint
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    # Add exception handlers
    @app.exception_handler(RecordNotFoundError)
    async def handle_record_not_found(request, exc: RecordNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DomainError)
    async def handle_domain_error(request, exc: DomainError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    # Add health check at root (for container health checks)
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Check service health."""
        return {
            "status": "healthy",
            "version": settings.app.version,
            "environment": settings.app.env,
        }
    
    # Also add health check under API v1 (for frontend)
    @app.get("/api/v1/health", tags=["Health"])
    async def api_health_check():
        """Check service health via API."""
        return {
            "status": "healthy",
            "version": settings.app.version,
            "environment": settings.app.env,
        }

    return app
