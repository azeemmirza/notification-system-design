import unittest
from datetime import datetime, timezone, timedelta

from src.notification_service import NotificationService
from src.providers.policy_pipeline import PolicyPipeline
from src.providers.default_dispatcher import DefaultDispatcher
from src.providers.default_router import DefaultRouter
from src.providers.dummy_provider import DummyProvider
from src.policies.validate_request_policy import ValidateRequestPolicy
from src.policies.scheduling_policy import SchedulingPolicy
from src.policies.retry_policy import RetryPolicy
from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SmsChannel
from src.channels.push_channel import PushChannel
from src.models.notification_request import NotificationRequest
from src.models.route import Route


class TestNotificationService(unittest.TestCase):
    # Test cases for NotificationService

    def setUp(self):
        # Set up test fixtures
        self.email_provider = DummyProvider("mailgun")
        self.sms_provider = DummyProvider("twilio")
        self.push_provider = DummyProvider("fcm")

        self.email_channel = EmailChannel()
        self.sms_channel = SmsChannel()
        self.push_channel = PushChannel()

        self.routes = {
            "email": Route(channel=self.email_channel, provider=self.email_provider),
            "sms": Route(channel=self.sms_channel, provider=self.sms_provider),
            "push": Route(channel=self.push_channel, provider=self.push_provider),
        }

        self.router = DefaultRouter(routes_by_channel=self.routes)
        self.dispatcher = DefaultDispatcher()
        self.pipeline = PolicyPipeline(
            policies=[
                ValidateRequestPolicy(),
                SchedulingPolicy(),
                RetryPolicy(max_attempts=2),
            ]
        )
        self.service = NotificationService(
            router=self.router,
            pipeline=self.pipeline,
            dispatcher=self.dispatcher
        )

    def test_send_immediate_email(self):
        # Test sending an immediate email notification
        req = NotificationRequest(
            id="test-1",
            recipient="user@example.com",
            message="Hello",
            priority=1,
            channel_hint="email",
        )
        receipt = self.service.send(req)

        self.assertEqual(receipt.status, "SENT")
        self.assertIsNotNone(receipt.provider_message_id)

    def test_send_immediate_sms(self):
        # Test sending an immediate SMS notification
        req = NotificationRequest(
            id="test-2",
            recipient="+15551234567",
            message="SMS Message",
            priority=0,
            channel_hint="sms",
        )
        receipt = self.service.send(req)

        self.assertEqual(receipt.status, "SENT")
        self.assertIsNotNone(receipt.provider_message_id)

    def test_send_immediate_push(self):
        # Test sending an immediate push notification
        req = NotificationRequest(
            id="test-3",
            recipient="device-token-xyz",
            message="Push Notification",
            priority=2,
            channel_hint="push",
        )
        receipt = self.service.send(req)

        self.assertEqual(receipt.status, "SENT")
        self.assertIsNotNone(receipt.provider_message_id)

    def test_validation_failure_empty_recipient(self):
        # Test validation failure when recipient is empty
        req = NotificationRequest(
            id="test-4",
            recipient="",
            message="Message",
            priority=0,
            channel_hint="email",
        )
        receipt = self.service.send(req)

        self.assertEqual(receipt.status, "FAILED")
        self.assertEqual(receipt.detail, "recipient is required")

    def test_default_channel_to_email(self):
        # Test that default channel is email
        req = NotificationRequest(
            id="test-5",
            recipient="user@example.com",
            message="Test",
            priority=1,
        )
        receipt = self.service.send(req)
        self.assertEqual(receipt.status, "SENT")


if __name__ == "__main__":
    unittest.main()

    def test_send_scheduled_notification(self):
        # Test sending a scheduled notification (future)
        future_time = datetime.now(timezone.utc) + timedelta(hours=1)
        req = NotificationRequest(
            id="test-6",
            recipient="user@example.com",
            message="Scheduled",
            priority=1,
            channel_hint="email",
            scheduled_at=future_time,
        )
        receipt = self.service.send(req)
        self.assertEqual(receipt.status, "SCHEDULED")

    def test_validation_failure_empty_message(self):
        req = NotificationRequest(
            id="test-7",
            recipient="user@example.com",
            message="",
            priority=0,
            channel_hint="email",
        )
        receipt = self.service.send(req)
        self.assertEqual(receipt.status, "FAILED")

    def test_validation_failure_negative_priority(self):
        req = NotificationRequest(
            id="test-8",
            recipient="user@example.com",
            message="Message",
            priority=-1,
            channel_hint="email",
        )
        receipt = self.service.send(req)
        self.assertEqual(receipt.status, "FAILED")

    def test_multiple_sequential_sends(self):
        # Test sending multiple notifications sequentially
        requests = [
            NotificationRequest(
                id=f"seq-{i}",
                recipient=f"user{i}@example.com",
                message=f"Message {i}",
                priority=i % 3,
                channel_hint="email",
            )
            for i in range(5)
        ]
        receipts = [self.service.send(req) for req in requests]
        for receipt in receipts:
            self.assertEqual(receipt.status, "SENT")

    def test_notification_with_special_characters(self):
        req = NotificationRequest(
            id="test-9",
            recipient="user+tag@example.com",
            message="Message with special chars !@#$%",
            priority=1,
            channel_hint="email",
        )
        receipt = self.service.send(req)
        self.assertEqual(receipt.status, "SENT")

    def test_notification_request_immutability(self):
        req = NotificationRequest(
            id="test-10",
            recipient="user@example.com",
            message="Message",
            priority=1,
        )
        with self.assertRaises(Exception):
            req.message = "Modified"
