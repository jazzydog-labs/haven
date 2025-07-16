"""Integration tests for main application entry point."""

from unittest.mock import patch


def test_main_entry_point():
    """Test the main entry point of the application."""
    from haven import main

    # Mock uvicorn.run to prevent actual server startup
    with patch("uvicorn.run") as mock_run:
        # Import and call main
        main.main()

        # Verify uvicorn.run was called with correct parameters
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args

        # Check the app parameter
        assert args[0] == "haven.interface.api.app:create_app"

        # Check other parameters
        assert kwargs.get("factory") is True
        assert kwargs.get("host") == "0.0.0.0"
        assert kwargs.get("port") == 8080
        assert kwargs.get("reload") is True
