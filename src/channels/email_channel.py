from typing import TYPE_CHECKING

from src.interfaces.channel import Channel

if TYPE_CHECKING:
    from src.interfaces.provider import Provider
    from src.models.notification_request import NotificationRequest
    from src.models.delivery_report import DeliveryReceipt


class EmailChannel(Channel):
    # Email channel implementation.
    
    def send(self, req: "NotificationRequest", provider: "Provider") -> "DeliveryReceipt":
        from src.models.delivery_report import DeliveryReceipt
        
        payload = {
            "to": req.recipient,
            "body": req.message,
            "priority": req.priority,
            "request_id": req.id,
            "channel": "email",
        }
        provider_message_id = provider.deliver(payload)
        return DeliveryReceipt(status="SENT", provider_message_id=provider_message_id)
