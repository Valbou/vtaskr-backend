import click

from flask import current_app
from flask.cli import with_appcontext
from src.notifications.models import Contact
from src.notifications.services import NotificationService
from src.notifications.settings import MessageType

from . import notification_cli_bp


@notification_cli_bp.cli.command("send_test_notification")
@click.argument("email", nargs=1, required=True)
@with_appcontext
def send_test_notification(email: list[str]):
    EVENT_NAME = "notifications:test:message"

    service = NotificationService(services=current_app.dependencies)
    contact = Contact(
        first_name="Foo",
        last_name="BAR",
        email=email,
    )

    service.add_new_contact(contact)
    service.subscribe(
        contact=contact, event_name=EVENT_NAME, event_type=MessageType.EMAIL
    )

    messages = service.build_messages(
        name="notifications:test:message", context={"targets": [contact.id]}
    )

    service.add_messages(messages=messages)
    service.notify_all()

    service.delete_contact(contact_id=contact.id)
