from src.interfaces.router import Router
from src.interfaces.dispatcher import Dispatcher
from src.providers.policy_pipeline import PolicyPipeline
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class NotificationService:
    # Main service for sending notifications through various channels.
    
    def __init__(self, router: Router, pipeline: PolicyPipeline, dispatcher: Dispatcher) -> None:
        self._router = router
        self._pipeline = pipeline
        self._dispatcher = dispatcher

    def send(self, req: NotificationRequest) -> DeliveryReceipt:
        # Send a notification request through the configured pipeline.
        route = self._router.resolve(req)

        def terminal(r: NotificationRequest) -> DeliveryReceipt:
            return self._dispatcher.dispatch(r, route)

        return self._pipeline.execute(req, terminal)
