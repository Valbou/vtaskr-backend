from src.notifications.settings import MessageType

from .messages import AbstractMessage


class MessageFabric:
    @classmethod
    def get_message_class(cls, message_type: MessageType) -> type[AbstractMessage]:
        for message_class in AbstractMessage.__subclasses__():
            if message_class.message_type is message_type:
                return message_class
