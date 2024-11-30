from src.notifications.exceptions import InvalidTemplateError
from src.notifications.settings import MessageType

from .abstract import AbstractTemplate


class TemplateFabric:
    def _get_complete_recursive_subclasses(self) -> list[type[AbstractTemplate]]:
        sub_classes = AbstractTemplate.__subclasses__()

        sub_c = sub_classes
        while sub_c:
            ssub = []
            for c in sub_c:
                sub_classes.extend(c.__subclasses__())
                ssub.extend(c.__subclasses__())

            sub_c = ssub

        return list(set(sub_classes))

    def get_template(self, template_type: MessageType, name: str) -> AbstractTemplate:
        try:
            return [
                c
                for c in self._get_complete_recursive_subclasses()
                if c.event_name == name and c.event_type is template_type
            ][0]()
        except IndexError:
            raise InvalidTemplateError(
                f"There is no {template_type} template for event {name}"
            )
