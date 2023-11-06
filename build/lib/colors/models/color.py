from re import fullmatch
from typing import TypeVar

from src.colors.exceptions.color import ColorFormatError

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
    def from_string(cls, colors: str) -> TColor | None:
        return Color(*colors.split("|"))

    @classmethod
    def check_format(cls, color) -> bool:
        match = fullmatch(r"^#[0-9A-Fa-f]{6}$", color)
        if match:
            return True
        return False
