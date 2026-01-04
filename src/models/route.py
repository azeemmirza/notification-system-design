from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interfaces.channel import Channel
    from src.interfaces.provider import Provider


@dataclass(frozen=True)
class Route:
    channel: "Channel"
    provider: "Provider"
