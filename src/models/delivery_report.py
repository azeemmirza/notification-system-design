from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DeliveryReceipt:
    status: str
    provider_message_id: Optional[str] = None
    detail: Optional[str] = None
