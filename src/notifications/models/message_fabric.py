from src.ports import AbstractMessage, MessageType


class MessageFabric:
    @classmethod
    def get_message_class(cls, event_type: MessageType) -> type[AbstractMessage]:
        for message_class in AbstractMessage.__subclasses__():
            if (message_class.message_type is event_type):
                return message_class
