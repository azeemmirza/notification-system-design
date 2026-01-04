from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.notification_request import NotificationRequest
    from src.models.route import Route
    from src.models.delivery_report import DeliveryReceipt


class Dispatcher(ABC):
    @abstractmethod
    def dispatch(self, req: "NotificationRequest", route: "Route") -> "DeliveryReceipt":
        # Execute the actual delivery via route.
        raise NotImplementedError
