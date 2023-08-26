import logging

from django.conf import settings

from main.business_logic.dates_controller import get_actual_dates
from main.models import AvailableTimeModel

logger = logging.getLogger(__name__)


def create_time_tables(at_data: dict[str, str] = settings.DEFAULT_AVAILABLE_TIME, dates: dict[str, str] = None) -> None:
    create_default_at_table(at_data)
    create_actual_at_table(at_data)
    create_dates_table(dates)
    logger.info("Basic time tables created.")
    print("Basic time tables created.")


def create_default_at_table(at_data: dict[str, str] = settings.DEFAULT_AVAILABLE_TIME) -> None:
    logger.info("Creating default timetable...")
    AvailableTimeModel.objects.create(time_type='default', **at_data)


def create_actual_at_table(at_data: dict[str, str] = settings.DEFAULT_AVAILABLE_TIME) -> None:
    logger.info("Creating actual timetable...")
    AvailableTimeModel.objects.create(time_type='actual', **at_data)


def create_dates_table(dates: dict[str, str] = None) -> None:
    logger.info("Creating dates timetable...")
    dates = get_actual_dates() if dates is None else dates
    AvailableTimeModel.objects.create(time_type='dates', **dates)
