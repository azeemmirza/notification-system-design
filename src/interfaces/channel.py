from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interfaces.provider import Provider
    from src.models.notification_request import NotificationRequest
    from src.models.delivery_report import DeliveryReceipt


class Channel(ABC):
    @abstractmethod
    def send(self, req: "NotificationRequest", provider: "Provider") -> "DeliveryReceipt":
        # Prepare payload and delegate to provider.
        raise NotImplementedError
