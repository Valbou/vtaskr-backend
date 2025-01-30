from dataclasses import dataclass

from src.libs.openapi.base import openapi
from src.notifications.models import Contact

CONTACT_COMPONENT = "#/components/schemas/Contact"

contact_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "telegram": {"type": "string"},
        "phone_number": {"type": "string"},
        "timezone": {"type": "string"},
        "locale": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
    },
    "required": ["email"],
}
openapi.register_schemas_components("Contact", contact_component)


@dataclass
class ContactDTO:
    first_name: str
    last_name: str
    email: str
    telegram: str = ""
    phone_number: str = ""
    timezone: str | None = None
    locale: str | None = None
    created_at: str = ""
    updated_at: str = ""
    id: str = ""


class ContactMapperDTO:
    @classmethod
    def model_to_dto(cls, contact: Contact) -> ContactDTO:
        return ContactDTO(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            telegram=contact.telegram,
            phone_number=contact.phone_number,
            timezone=contact.timezone,
            locale=contact.locale,
            created_at=contact.created_at.isoformat(),
            updated_at=contact.updated_at.isoformat(),
        )

    @classmethod
    def dto_to_model(
        cls, contact_dto: ContactDTO, contact: Contact | None = None
    ) -> Contact:

        if not contact:
            contact = Contact(
                first_name=contact_dto.first_name,
                last_name=contact_dto.last_name,
                email=contact_dto.email,
                telegram=contact_dto.telegram,
                phone_number=contact_dto.phone_number,
                timezone=contact_dto.timezone,
                locale=contact_dto.locale,
            )
        else:
            contact.email = contact_dto.email
            contact.telegram = contact_dto.telegram
            contact.phone_number = contact_dto.phone_number
            contact.timezone = contact_dto.timezone
            contact.locale = contact_dto.locale

        return contact
