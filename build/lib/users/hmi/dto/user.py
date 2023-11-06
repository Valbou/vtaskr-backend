from dataclasses import dataclass

from babel import Locale

from src.libs.openapi.base import openapi
from src.users.models import User

USER_COMPONENT = "#/components/schemas/User"

user_component = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "locale": {"type": "string"},
        "timezone": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "last_login_at": {"type": "string", "format": "date-time"},
    },
    "required": ["first_name", "last_name", "email", "locale", "timezone"],
}
openapi.register_schemas_components("User", user_component)


@dataclass
class UserDTO:
    id: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    locale: str = ""
    timezone: str = ""
    created_at: str = ""
    last_login_at: str = ""


class UserMapperDTO:
    @classmethod
    def model_to_dto(cls, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            locale=str(user.locale),
            timezone=user.timezone,
            created_at=user.created_at.isoformat(),
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else "",
        )

    @classmethod
    def dto_to_model(cls, user_dto: UserDTO, user: User) -> User:
        user.first_name = user_dto.first_name
        user.last_name = user_dto.last_name
        user.locale = Locale.parse(user_dto.locale)
        user.timezone = user_dto.timezone
        return user
