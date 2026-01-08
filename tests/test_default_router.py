import unittest

from src.providers.default_router import DefaultRouter
from src.channels.email_channel import EmailChannel
from src.channels.sms_channel import SmsChannel
from src.providers.dummy_provider import DummyProvider
from src.models.notification_request import NotificationRequest
from src.models.route import Route


class TestDefaultRouter(unittest.TestCase):
    # Test cases for DefaultRouter

    def setUp(self):
        self.email_provider = DummyProvider("mailgun")
        self.sms_provider = DummyProvider("twilio")

        self.email_channel = EmailChannel()
        self.sms_channel = SmsChannel()

        self.routes = {
            "email": Route(channel=self.email_channel, provider=self.email_provider),
            "sms": Route(channel=self.sms_channel, provider=self.sms_provider),
        }

        self.router = DefaultRouter(routes_by_channel=self.routes)

    def test_resolve_email_route(self):
        req = NotificationRequest(
            id="test-1",
            recipient="user@example.com",
            message="Message",
            priority=0,
            channel_hint="email",
        )
        route = self.router.resolve(req)
        self.assertEqual(route.channel, self.email_channel)

    def test_default_to_email_route(self):
        req = NotificationRequest(
            id="test-2",
            recipient="user@example.com",
            message="Message",
            priority=0,
            channel_hint=None,
        )
        route = self.router.resolve(req)
        self.assertEqual(route.channel, self.email_channel)


if __name__ == "__main__":
    unittest.main()
