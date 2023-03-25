from re import fullmatch
from uuid import uuid4
from datetime import datetime
from typing import Optional, TypeVar
from dataclasses import dataclass


class ColorFormatError(Exception):
    pass


TColor = TypeVar("TColor", bound="Color")


class Color:
    background: str
    text: str

    def __init__(self, background: str, text: str) -> None:
        if Color.check_format(background) and Color.check_format(text):
            self.background = background
            self.text = text
        else:
            raise ColorFormatError

    def __str__(self) -> str:
        return f"{self.background}|{self.text}"

    @classmethod
    def from_string(cls, colors: str) -> TColor:
        return Color(*colors.split("|"))

    @classmethod
    def check_format(cls, color) -> bool:
        match = fullmatch(r"^#[0-9A-Fa-f]{6}$", color)
        if match:
            return True
        return False


@dataclass
class Tag:
    id: str = ""
    created_at: Optional[datetime] = None
    title: str = ""
    color: Optional[Color] = None

    def __init__(
        self,
        title: str,
        color: Optional[Color] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id or uuid4().hex
        self.created_at = created_at or datetime.now()
        self.title = title
        self.color = color
