import click

from flask import current_app
from flask.cli import with_appcontext
from src.notifications.services import NotificationService
from src.notifications.settings import MessageType

from . import logger, notification_cli_bp


@notification_cli_bp.cli.command("register_new_subscription")
@click.argument("email", nargs=1, required=True)
@click.argument("event_name", nargs=1, required=True)
@with_appcontext
def register_new_subscription(email: str, event_name: str):
    service = NotificationService(services=current_app.dependencies)
    contact = service.get_contact_from_email(email=email)

    if contact:
        service.subscribe(
            contact=contact, event_name=event_name, event_type=MessageType.EMAIL
        )

        logger.info(
            f"Contact {contact.first_name} {contact.last_name} "
            "now listen to {event_name} event"
        )

    else:
        logger.error(f"No contact found with email {email}")
