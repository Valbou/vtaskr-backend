from datetime import datetime
from zoneinfo import ZoneInfo

from flask.cli import with_appcontext
from src.events.jobs.tasks import celery_health_check

from . import events_cli_bp


@events_cli_bp.cli.command("celery_health_check")
@with_appcontext
def celery_ping():
    """Just to check celery communication"""

    now = datetime.now(tz=ZoneInfo("UTC"))
    celery_health_check.delay(f"Check {now.isoformat()}")
