from dataclasses import dataclass
from typing import TypeVar

from src.libs.sqlalchemy.base_model import BaseModelUpdate
from src.ports import MessageType

TSubscription = TypeVar("TSubscription", bound="Subscription")


@dataclass
class Subscription(BaseModelUpdate):
    """To receive notifications"""

    event_type: MessageType
    event_name: str
    tenant_id: str
    to: str
    cc: str = ""  # coma separated values
    bcc: str = ""  # coma separated values

    @classmethod
    def temp_template_from_context(cls, context: dict) -> TSubscription:
        return Subscription(
            event_type=context.pop("message_type"),
            event_name="None",
            tenant_id=context.pop("tenant_id"),
            to=context.pop("to"),
            cc="",
            bcc="",
        )
