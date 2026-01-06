from typing import Callable

from src.interfaces.policy import Policy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class ValidateRequestPolicy(Policy):
    # Validates the notification request before processing.
    
    def apply(
        self,
        req: NotificationRequest,
        next_: Callable[[NotificationRequest], DeliveryReceipt],
    ) -> DeliveryReceipt:
        if not req.recipient.strip():
            return DeliveryReceipt(status="FAILED", detail="recipient is required")
        if not req.message.strip():
            return DeliveryReceipt(status="FAILED", detail="message is required")
        if req.priority < 0:
            return DeliveryReceipt(status="FAILED", detail="priority must be >= 0")
        return next_(req)
