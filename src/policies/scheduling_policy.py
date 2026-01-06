from typing import Callable
from datetime import datetime, timezone

from src.interfaces.policy import Policy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class SchedulingPolicy(Policy):
    # If scheduled_at is in the future, short-circuit and mark as SCHEDULED.
    # Real systems would enqueue to a job queue instead.
    
    def apply(
        self,
        req: NotificationRequest,
        next_: Callable[[NotificationRequest], DeliveryReceipt],
    ) -> DeliveryReceipt:
        if req.scheduled_at is None:
            return next_(req)

        now = datetime.now(timezone.utc)
        scheduled = req.scheduled_at
        if scheduled.tzinfo is None:
            scheduled = scheduled.replace(tzinfo=timezone.utc)

        if scheduled > now:
            return DeliveryReceipt(
                status="SCHEDULED",
                detail=f"Notification scheduled for {scheduled.isoformat()}"
            )
        return next_(req)
