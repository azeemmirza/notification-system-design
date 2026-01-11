from src.notification_service import NotificationService
from src.providers.default_router import DefaultRouter
from src.providers.default_dispatcher import DefaultDispatcher
from src.providers.policy_pipeline import PolicyPipeline
from src.providers.dummy_provider import DummyProvider
from src.policies.validate_request_policy import ValidateRequestPolicy
from src.policies.scheduling_policy import SchedulingPolicy
from src.policies.retry_policy import RetryPolicy
from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SmsChannel
from src.channels.push_channel import PushChannel
from src.models.notification_request import NotificationRequest
from src.models.route import Route
from datetime import datetime, timezone, timedelta


def main():
    # Setup providers
    email_provider = DummyProvider("mailgun")
    sms_provider = DummyProvider("twilio")
    push_provider = DummyProvider("fcm")

    # Setup channels
    email_channel = EmailChannel()
    sms_channel = SmsChannel()
    push_channel = PushChannel()

    # Setup routes
    routes = {
        "email": Route(channel=email_channel, provider=email_provider),
        "sms": Route(channel=sms_channel, provider=sms_provider),
        "push": Route(channel=push_channel, provider=push_provider),
    }

    # Setup service
    router = DefaultRouter(routes_by_channel=routes)
    dispatcher = DefaultDispatcher()
    pipeline = PolicyPipeline(policies=[
        ValidateRequestPolicy(),
        SchedulingPolicy(),
        RetryPolicy(max_attempts=2),
    ])
    service = NotificationService(router=router, pipeline=pipeline, dispatcher=dispatcher)

    print("=== Notification System Demo ===\n")

    # Example 1: Immediate email
    print("1. Sending immediate email...")
    req1 = NotificationRequest(
        id="msg-001",
        recipient="user@example.com",
        message="Welcome to our service!",
        priority=1,
        channel_hint="email"
    )
    receipt1 = service.send(req1)
    print(f"   Status: {receipt1.status}, ID: {receipt1.provider_message_id}\n")

    # Example 2: SMS notification
    print("2. Sending SMS...")
    req2 = NotificationRequest(
        id="msg-002",
        recipient="+1234567890",
        message="Your verification code is 123456",
        priority=2,
        channel_hint="sms"
    )
    receipt2 = service.send(req2)
    print(f"   Status: {receipt2.status}, ID: {receipt2.provider_message_id}\n")

    # Example 3: Push notification
    print("3. Sending push notification...")
    req3 = NotificationRequest(
        id="msg-003",
        recipient="device-token-xyz",
        message="New message from your friend",
        priority=1,
        channel_hint="push"
    )
    receipt3 = service.send(req3)
    print(f"   Status: {receipt3.status}, ID: {receipt3.provider_message_id}\n")

    # Example 4: Scheduled notification
    print("4. Sending scheduled notification...")
    future_time = datetime.now(timezone.utc) + timedelta(hours=2)
    req4 = NotificationRequest(
        id="msg-004",
        recipient="user@example.com",
        message="Reminder: Your appointment is in 2 hours",
        priority=2,
        channel_hint="email",
        scheduled_at=future_time
    )
    receipt4 = service.send(req4)
    print(f"   Status: {receipt4.status}, Detail: {receipt4.detail}\n")

    # Example 5: Validation failure
    print("5. Testing validation failure...")
    req5 = NotificationRequest(
        id="msg-005",
        recipient="",
        message="This should fail",
        priority=1,
        channel_hint="email"
    )
    receipt5 = service.send(req5)
    print(f"   Status: {receipt5.status}, Detail: {receipt5.detail}\n")

    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()
