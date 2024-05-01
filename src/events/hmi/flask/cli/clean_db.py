from sqlalchemy import text

from flask import current_app
from flask.cli import with_appcontext

from . import event_cli_bp


@event_cli_bp.cli.command("clean_events_data")
@with_appcontext
def clean_events_data():
    with current_app.dependencies.persistence.get_session() as session:
        statement = text("TRUNCATE TABLE events CASCADE;")
        session.execute(statement)
        session.commit()
        print("SQL event tables cleaned.")
