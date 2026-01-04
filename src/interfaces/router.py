from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.notification_request import NotificationRequest
    from src.models.route import Route


class Router(ABC):
    @abstractmethod
    def resolve(self, req: "NotificationRequest") -> "Route":
        # Choose a route (channel + provider) for the given request.
        raise NotImplementedError
