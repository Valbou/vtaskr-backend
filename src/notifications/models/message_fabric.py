from src.ports import AbstractMessage, MessageType


class MessageFabric:
    @classmethod
    def get_base_message_class(cls, event_type: MessageType) -> type[AbstractMessage]:
        for message_class in AbstractMessage.__subclasses__():
            if (
                message_class.__name__.lower()
                == f"base{event_type.value.lower()}content"
            ):
                return message_class
