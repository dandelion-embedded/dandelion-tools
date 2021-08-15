from time import time
class DandelionDeviceManifest:
    """Device manifest (dandelion.json)."""

    # Dandelion Core version
    version: str

    def __init__(self, version: str) -> None:
        self.version = version