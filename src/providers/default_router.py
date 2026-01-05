from typing import Dict

from src.interfaces.router import Router
from src.models.notification_request import NotificationRequest
from src.models.route import Route


class DefaultRouter(Router):
    # Simple routing rules:
    # - If req.channel_hint is present, use it.
    # - Otherwise default to 'email'.

    def __init__(self, routes_by_channel: Dict[str, Route]) -> None:
        self._routes_by_channel = routes_by_channel

    def resolve(self, req: NotificationRequest) -> Route:
        channel_key = (req.channel_hint or "email").lower()
        if channel_key not in self._routes_by_channel:
            raise ValueError(f"No route configured for channel: {channel_key}")
        return self._routes_by_channel[channel_key]
