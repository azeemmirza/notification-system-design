import unittest
from datetime import datetime, timezone, timedelta

from src.policies.validate_request_policy import ValidateRequestPolicy
from src.policies.scheduling_policy import SchedulingPolicy
from src.policies.retry_policy import RetryPolicy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class TestPolicies(unittest.TestCase):
    # Test cases for policies

    def test_validate_request_policy_valid(self):
        policy = ValidateRequestPolicy()
        req = NotificationRequest(
            id="test-1",
            recipient="user@example.com",
            message="Valid",
            priority=0,
        )
        result = policy.apply(req, lambda r: DeliveryReceipt(status="SENT"))
        self.assertEqual(result.status, "SENT")

    def test_validate_request_policy_empty_recipient(self):
        policy = ValidateRequestPolicy()
        req = NotificationRequest(
            id="test-2",
            recipient="",
            message="Message",
            priority=0,
        )
        result = policy.apply(req, lambda r: DeliveryReceipt(status="SENT"))
        self.assertEqual(result.status, "FAILED")

    def test_scheduling_policy_future(self):
        policy = SchedulingPolicy()
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        req = NotificationRequest(
            id="test-3",
            recipient="user@example.com",
            message="Message",
            priority=0,
            scheduled_at=future,
        )
        result = policy.apply(req, lambda r: DeliveryReceipt(status="SENT"))
        self.assertEqual(result.status, "SCHEDULED")


if __name__ == "__main__":
    unittest.main()
