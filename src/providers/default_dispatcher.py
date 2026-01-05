from src.interfaces.dispatcher import Dispatcher
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt
from src.models.route import Route


class DefaultDispatcher(Dispatcher):
    # Default implementation of Dispatcher.
    
    def dispatch(self, req: NotificationRequest, route: Route) -> DeliveryReceipt:
        return route.channel.send(req, route.provider)
