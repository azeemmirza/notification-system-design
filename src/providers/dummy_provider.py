from src.interfaces.provider import Provider
from typing import Any, Dict
import uuid


import uuid
class DummyProvider(Provider):
    # A fake provider for demos/tests.
    
    def __init__(self, name: str) -> None:
        self._name = name

    def deliver(self, payload: Dict[str, Any]) -> str:
        # Generate a fake message ID
        msg_id = f"{self._name}-{str(uuid.uuid4())[:8]}"
        return msg_id
