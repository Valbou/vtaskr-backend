from typing import Generator


def split_by(iterable: list, size: int) -> Generator:
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]  # noqa: E203
