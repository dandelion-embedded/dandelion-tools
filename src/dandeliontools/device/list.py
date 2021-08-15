import logging
from typing import List

from rich.progress import track
from serial.tools import list_ports

from dandeliontools.device import DandelionDevice


def list_devices(show_progress: bool = False) -> List[DandelionDevice]:
    """Lists all Dandelion devices."""

    ports = list_ports.comports()
    logging.debug(f"Found {len(ports)} serial ports.")

    dandelion_devices: List[DandelionDevice] = []

    # Iterate over all ports and try to connect to a Dandelion device.
    if show_progress:
        for n in track(range(len(ports)), "Discovering serial devices", transient=True):
            try:
                device = DandelionDevice(ports[n])
                dandelion_devices.append(device)
            except BaseException as e:
                logging.debug(f"Skipping port {ports[n].device} due to error: {e}")
                continue

            logging.debug(f"Discovered a device at {device.__pyboard.serial.portstr}.")
    else:

        # Silent mode.
        for port in ports:
            try:
                device = DandelionDevice(port)
                dandelion_devices.append(device)
            except:
                continue

    return dandelion_devices
