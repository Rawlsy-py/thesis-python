"""FastAPI Benchmarking App."""

import typer
import uvicorn

cli = typer.Typer()


@cli.command()
def runserver(
    host: str = "127.0.0.1",
    port: int = 8000,
    debug: bool = typer.Option(False, help="Run in debug mode"),
):
    """
    Start the FastAPI application.

    Args:
        host (str): The host IP to run the FastAPI server on.
        port (int): The port to run the FastAPI server on.
        debug (bool): If True, the server will be started in debug mode with live reloading.
    """
    uvicorn.run(
        "your_package_name.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info",
    )


if __name__ == "__main__":
    cli()
