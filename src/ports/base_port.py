from abc import ABC


class InjectablePort(ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__()

    def set_context(self, **ctx) -> None:
        pass
