from abc import ABC, abstractmethod
from typing import Any, Dict


class Provider(ABC):
    @abstractmethod
    def deliver(self, payload: Dict[str, Any]) -> str:
        # Deliver payload and return provider message id.
        raise NotImplementedError
