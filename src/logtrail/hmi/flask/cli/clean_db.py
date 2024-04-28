from sqlalchemy import text

from flask import current_app
from flask.cli import with_appcontext

from . import logtrail_cli_bp


@logtrail_cli_bp.cli.command("clean_logtrails_data")
@with_appcontext
def clean_logtrails_data():
    with current_app.dependencies.persistence.get_session() as session:
        statement = text("TRUNCATE TABLE logtrails CASCADE;")
        session.execute(statement)
        session.commit()
        print("SQL LogTrail tables cleaned.")
