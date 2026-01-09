import unittest

from src.providers.policy_pipeline import PolicyPipeline
from src.policies.validate_request_policy import ValidateRequestPolicy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class TestPolicyPipeline(unittest.TestCase):
    # Test cases for PolicyPipeline

    def test_empty_pipeline(self):
        pipeline = PolicyPipeline(policies=[])
        req = NotificationRequest(
            id="test-1",
            recipient="user@example.com",
            message="Message",
            priority=0,
        )
        result = pipeline.execute(req, lambda r: DeliveryReceipt(status="SENT"))
        self.assertEqual(result.status, "SENT")

    def test_single_policy_pipeline(self):
        pipeline = PolicyPipeline(policies=[ValidateRequestPolicy()])
        req = NotificationRequest(
            id="test-2",
            recipient="user@example.com",
            message="Message",
            priority=0,
        )
        result = pipeline.execute(req, lambda r: DeliveryReceipt(status="SENT"))
        self.assertEqual(result.status, "SENT")


if __name__ == "__main__":
    unittest.main()
