import click
import logging

from dandeliontools.customlogging import setup_logging
from dandeliontools.list import list_devices


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def cli(verbose):
    """
    \b
    * Dandelion Tools *
    Tools for communicating with Dandelion Core boards.
    """

    setup_logging(verbose=verbose)
    logging.debug("Verbose mode enabled.")


@cli.command()
def list():
    """Lists the detected Dandelion boards."""

    logging.debug("Requesting serial port list.")
    list_devices()

@cli.command()
@click.option("-p", "--port", default=None, help="Serial port to connect to.", prompt=True, metavar="<PORT>")
def install(port):
    """Installs Dandelion Core to a Micropython-enabled board."""

    logging.debug(f"Installing Dandelion Core to device connected at {port}.")