import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from creator import creator


logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()

weekly_trigger = CronTrigger(
    day_of_week="sun",
    hour=23,
    minute=59,
    timezone="Europe/Istanbul",
)

daily_trigger = CronTrigger(
    hour=0,
    minute=5,
    timezone="Europe/Istanbul",
)

test_trigger = CronTrigger(
    minute=10
)

scheduler.add_job(
    func=creator.get_all_zodiacs_articles,
    trigger=test_trigger,
    # max_instances=1,
    # coalesce=True,
)
