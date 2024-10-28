from dataclasses import dataclass
from typing import Self

from src.libs.sqlalchemy.base_model import BaseModelUpdate
from src.ports import MessageType

from .contact import Contact


@dataclass
class Subscription(BaseModelUpdate):
    """To receive notifications"""

    event_type: MessageType
    event_name: str
    contact_id: str
    contact: Contact

    @classmethod
    def temp_subscription_from_context(cls, context: dict) -> Self:
        return Subscription(
            event_type=context.get("message_type"),
            event_name="None",
            contact_id=context.get("tenant_id"),
            contact=Contact(
                id=context.pop("tenant_id"),
                email=context.pop("email", ""),
                telegram=context.pop("telegram", ""),
                phone_number=context.pop("phone_number", ""),
            ),
        )
