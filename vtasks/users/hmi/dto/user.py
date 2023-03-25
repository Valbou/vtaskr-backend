from dataclasses import dataclass, asdict

from babel import Locale

from vtasks.users.models import User


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
        if user_dto.first_name:
            user.first_name = user_dto.first_name
        if user_dto.last_name:
            user.last_name = user_dto.last_name
        if user_dto.locale:
            user.locale = Locale.parse(user_dto.locale)
        if user_dto.timezone:
            user.timezone = user_dto.timezone
        return user

    @classmethod
    def dto_to_dict(cls, user_dto: UserDTO) -> dict:
        return asdict(user_dto)
