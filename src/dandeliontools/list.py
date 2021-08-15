import logging
from typing import List

from rich.console import Console
from rich.progress import track
from rich.table import Table
from serial.tools import list_ports
from timeout_decorator import timeout

from dandeliontools.ampy.pyboard import Pyboard
from dandeliontools.device import DandelionDevice

from .ampy.files import Files


def list_devices():
    """Lists all Dandelion devices."""

    ports = list_ports.comports()
    logging.debug(f"Found {len(ports)} serial ports.")

    dandelion_devices: List[DandelionDevice] = []

    # Iterate over all ports and try to connect to a Dandelion device.
    for n in track(range(len(ports)), "Discovering serial devices", transient=True):
        try:
            device = DandelionDevice(ports[n])
        except BaseException as e:
            logging.debug(f"Skipping port {ports[n].device} due to error: {e}")
            continue

        dandelion_devices.append(device)
        logging.debug(f"Discovered a device at {device.pyboard.serial.portstr}.")

    # If no devices were found, print a warning and exit.
    if not dandelion_devices:
        logging.warning("No devices found.")
        return

    # Present the found devices in a rich table.
    table = Table(show_header=True)
    table.add_column("Port")
    table.add_column("Serial number")
    table.add_column("Dandelion version")

    for device in dandelion_devices:
        table.add_row(
            device.pyboard.serial.portstr,
            device.get_device_id(),
            device.manifest.version,
        )

    Console().print(table)
