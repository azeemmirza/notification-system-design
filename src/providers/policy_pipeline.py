from typing import Callable, Iterable, List

from src.interfaces.policy import Policy
from src.models.notification_request import NotificationRequest
from src.models.delivery_report import DeliveryReceipt


class PolicyPipeline:
    # Executes a chain of policies using the chain-of-responsibility pattern.
    
    def __init__(self, policies: Iterable[Policy]) -> None:
        self._policies: List[Policy] = list(policies)

    def execute(
        self,
        req: NotificationRequest,
        terminal: Callable[[NotificationRequest], DeliveryReceipt],
    ) -> DeliveryReceipt:
        # Compose policies around terminal (chain-of-responsibility).

        def make_chain(index: int) -> Callable[[NotificationRequest], DeliveryReceipt]:
            if index >= len(self._policies):
                return terminal

            policy = self._policies[index]

            def step(r: NotificationRequest) -> DeliveryReceipt:
                return policy.apply(r, make_chain(index + 1))

            return step

        return make_chain(0)(req)
