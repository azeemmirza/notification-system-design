from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class NotificationRequest:
    id: str
    recipient: str
    message: str
    priority: int = 0
    scheduled_at: Optional[datetime] = None
    channel_hint: Optional[str] = None
