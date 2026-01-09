import unittest

from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SmsChannel
from src.channels.push_channel import PushChannel
from src.providers.dummy_provider import DummyProvider
from src.models.notification_request import NotificationRequest


class TestChannels(unittest.TestCase):
    # Test cases for channel implementations

    def setUp(self):
        self.email_channel = EmailChannel()
        self.sms_channel = SmsChannel()
        self.push_channel = PushChannel()
        self.provider = DummyProvider("test-provider")

    def test_email_channel(self):
        req = NotificationRequest(
            id="test-1",
            recipient="user@example.com",
            message="Test",
            priority=1,
        )
        receipt = self.email_channel.send(req, self.provider)
        self.assertEqual(receipt.status, "SENT")

    def test_sms_channel(self):
        req = NotificationRequest(
            id="test-2",
            recipient="+15551234567",
            message="SMS",
            priority=0,
        )
        receipt = self.sms_channel.send(req, self.provider)
        self.assertEqual(receipt.status, "SENT")

    def test_push_channel(self):
        req = NotificationRequest(
            id="test-3",
            recipient="device-token",
            message="Push",
            priority=2,
        )
        receipt = self.push_channel.send(req, self.provider)
        self.assertEqual(receipt.status, "SENT")


if __name__ == "__main__":
    unittest.main()
