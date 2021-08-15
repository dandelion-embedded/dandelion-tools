import logging
from rich.logging import RichHandler
from rich.traceback import install


def setup_logging(verbose=False):
    """Sets the handler for logging and for tracebacks to rich."""

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=(logging.DEBUG if verbose else logging.INFO),
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )

    install(show_locals=True)
