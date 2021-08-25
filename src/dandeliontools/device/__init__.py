import json
from pathlib import Path

from dandeliontools.ampy.files import Files
from dandeliontools.ampy.pyboard import Pyboard
from dandeliontools.device.manifest import DandelionDeviceManifest
from serial.tools.list_ports_common import ListPortInfo
from timeout_decorator import timeout


class DandelionDevice:
    """Represents a Dandelion board."""

    __pyboard: Pyboard
    __files: Files
    manifest: DandelionDeviceManifest
    

    def to_json(self) -> dict:
        """Convert to JSON."""
        return {
            "port": self.get_port_name(),
            "id": self.get_device_id(),
            "manifest": self.manifest.to_json(),
        }

    @timeout(2)
    def __init__(self, port: ListPortInfo) -> None:
        """Initializes the Dandelion device.

        Args:
          port: The serial port to use.
        """

        self.__pyboard = Pyboard(port.device)
        self.__files = Files(self.__pyboard)

        # Try to load the manifest from the board.
        dandelion_json = self.__files.get("dandelion.json")
        manifest_dict = json.loads(dandelion_json)
        self.manifest = DandelionDeviceManifest(**manifest_dict)

    @timeout(1)
    def get_device_id(self) -> str:
        """Returns the device id.

        Returns:
          The device id.
        """

        here = Path(__file__).parent
        script = here / "onboard_scripts/get_device_id.py"

        self.__pyboard.enter_raw_repl()
        res = self.__pyboard.execfile(script)
        self.__pyboard.exit_raw_repl()

        # Due to serial transmission, we need to strip the string twice.
        # It is send as: b"b'<ID>'\r\n" (bytes).
        return str(res, "utf-8").strip().lstrip("b'").rstrip("'")

    def get_port_name(self) -> str:
        """Returns the port name.

        Returns:
          The port name.
        """

        return self.__pyboard.serial.portstr

    def get_status(self) -> dict:
        """Returns the status of the device as a dictionary.

        Returns:
          The status of the device.
        """

        here = Path(__file__).parent
        script = here / "onboard_scripts/get_device_status.py"

        self.__pyboard.enter_raw_repl()
        res = self.__pyboard.execfile(script)
        self.__pyboard.exit_raw_repl()

        # Due to serial transmission, we need to strip the string twice.
        # It is send as: b"b'<ID>'\r\n" (bytes).
        return json.loads(res)
