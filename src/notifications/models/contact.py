from dataclasses import dataclass

from src.libs.sqlalchemy.base_model import BaseModelUpdate


@dataclass
class Contact(BaseModelUpdate):
    """
    To send notification informations

    tenant_id is used as an id.
    tenant_id may be a user id or a group id
    (mailing list, group telegram with many readers...)
    """

    email: str = ""
    telegram: str = ""
    phone_number: str = ""
