import logging

import json
import click
from rich import prompt
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from serial.tools import list_ports

from dandeliontools.customlogging import setup_logging
from dandeliontools.device.list import list_devices


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.option("--json-output", is_flag=True, help="Enables JSON output.")
@click.pass_context
def cli(ctx: dict, verbose: bool, json_output: bool):
    """
    \b
    * Dandelion Tools *
    Tools for communicating with Dandelion Core boards.
    """

    ctx.ensure_object(dict)
    ctx.obj["JSON_OUTPUT"] = json_output

    # In case of json output, we need to setup the logger in order not to print unnecessary messages.
    if json_output:
        logging.basicConfig(level=logging.WARNING)
        return

    setup_logging(verbose=verbose)
    logging.debug("Verbose mode enabled.")


@cli.command()
@click.pass_context
def list(ctx):
    """Lists the detected Dandelion boards."""

    json_output: bool = ctx.obj["JSON_OUTPUT"] or False

    logging.debug("Requesting serial port list.")
    devices = list_devices(show_progress=not json_output)

    # Only print JSON output if the user requested it. Then exit.
    if json_output:
        click.echo(json.dumps([device.to_json() for device in devices], indent=4))
        return

    # If no devices were found, print a warning and exit.
    if not devices:
        logging.warning("No devices found.")
        return

    # Present the found devices in a rich table.
    table = Table(show_header=True)
    table.add_column("Port")
    table.add_column("Serial number")
    table.add_column("Dandelion version")

    for device in devices:
        table.add_row(
            device.get_port_name(),
            device.get_device_id(),
            device.manifest.version,
        )

    Console().print(table)
