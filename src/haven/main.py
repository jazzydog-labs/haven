"""Main entry point for Haven application."""

import uvicorn

from haven.config import get_settings
from haven.interface.api.app import create_app


def main() -> None:
    """Run the Haven application."""
    settings = get_settings()
    app = create_app()
    
    uvicorn.run(
        app,
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        log_level=settings.logging.level.lower(),
    )


if __name__ == "__main__":
    main()