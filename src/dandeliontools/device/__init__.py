import json
from pathlib import Path

from dandeliontools.ampy.files import Files
from dandeliontools.ampy.pyboard import Pyboard
from dandeliontools.device.manifest import DandelionDeviceManifest
from serial.tools.list_ports_common import ListPortInfo
from timeout_decorator import timeout


class DandelionDevice:
    """Represents a Dandelion board."""

    pyboard: Pyboard
    files: Files
    manifest: DandelionDeviceManifest

    @timeout(2)
    def __init__(self, port: ListPortInfo) -> None:
        """Initializes the Dandelion device.

        Args:
          port: The serial port to use.
        """

        self.pyboard = Pyboard(port.device)
        self.files = Files(self.pyboard)

        # Try to load the manifest from the board.
        dandelion_json = self.files.get("dandelion.json")
        manifest_dict = json.loads(dandelion_json)
        self.manifest = DandelionDeviceManifest(**manifest_dict)

    @timeout(1)
    def get_device_id(self) -> str:
        """Returns the device id.

        Returns:
          The device id.
        """

        here = Path(__file__).parent
        script = here/"onboard_scripts/get_device_id.py"

        self.pyboard.enter_raw_repl()
        res = self.pyboard.execfile(script)
        self.pyboard.exit_raw_repl()

        # Due to serial transmission, we need to strip the string twice.
        # It is send as: b"b'<ID>'\r\n" (bytes).
        return str(res, 'utf-8').strip().lstrip("b'").rstrip("'")