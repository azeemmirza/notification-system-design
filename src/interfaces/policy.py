from abc import ABC, abstractmethod
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.notification_request import NotificationRequest
    from src.models.delivery_report import DeliveryReceipt


class Policy(ABC):
    @abstractmethod
    def apply(
        self,
        req: "NotificationRequest",
        next_: Callable[["NotificationRequest"], "DeliveryReceipt"],
    ) -> "DeliveryReceipt":
        # Apply policy logic, then call next_ (or short-circuit).
        raise NotImplementedError
