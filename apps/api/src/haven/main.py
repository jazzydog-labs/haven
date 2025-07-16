"""Main entry point for Haven application."""

import uvicorn

from haven.config import get_settings
from haven.interface.api.app import create_app

# Create app instance for uvicorn to find
app = create_app()


def main() -> None:
    """Run the Haven application."""
    settings = get_settings()

    # Use import string when reload is enabled
    if settings.server.reload:
        app_str = "haven.main:app"
        factory = False
    else:
        app_str = app
        factory = False

    uvicorn.run(
        app_str,
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
        log_level=settings.logging.level.lower(),
        factory=factory,
    )


if __name__ == "__main__":
    main()
