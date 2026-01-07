from typing import Callable, Optional

from src.interfaces.policy import Policy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class RetryPolicy(Policy):
    # Very simple retry: retries on FAILED status up to max_attempts.
    # In real systems, you'd only retry on transient errors.
    
    def __init__(self, max_attempts: int = 3) -> None:
        self._max_attempts = max_attempts

    def apply(
        self,
        req: NotificationRequest,
        next_: Callable[[NotificationRequest], DeliveryReceipt],
    ) -> DeliveryReceipt:
        last: Optional[DeliveryReceipt] = None
        for _ in range(self._max_attempts):
            last = next_(req)
            if last.status != "FAILED":
                return last
        return last if last else DeliveryReceipt(status="FAILED", detail="retry policy failed unexpectedly")
