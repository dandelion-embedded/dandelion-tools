import json


class DandelionDeviceManifest:
    """Device manifest (dandelion.json)."""

    # Dandelion Core version
    version: str

    def to_json(self) -> dict:
        """Convert to JSON."""
        return {
            "version": self.version
        }

    def __init__(self, version: str) -> None:
        self.version = version