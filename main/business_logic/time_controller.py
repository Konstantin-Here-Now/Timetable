import datetime
import logging

from main.business_logic.available_time import AvailableTime
from main.business_logic.available_time_controller import get_available_time
from main.business_logic.dates_controller import get_day_from_date
from main.business_logic.exceptions import AvailableTimeExceeded
from main.business_logic.time_range import TimeRange
from main.models import Lesson

logger = logging.getLogger(__name__)


def is_time_available_globally(day_date: datetime.date, tr: TimeRange) -> bool:
    logger.info("Checking whether time is available globally...")
    day_name = get_day_from_date(day_date)
    return _is_correspond_to_default_at(day_name, tr) and not _is_already_occupied(day_date, tr)


def _is_correspond_to_default_at(day: str, tr: TimeRange) -> bool:
    default_available_time = get_available_time(time_type="default")
    day_at = AvailableTime(default_available_time[day])
    try:
        day_at.insert(tr)
        return True
    except AvailableTimeExceeded:
        return False


def _is_already_occupied(day_date: datetime.date, tr: TimeRange) -> bool:
    lessons = Lesson.objects.filter(date_lesson=day_date, approved=True)
    if lessons:
        for lesson in lessons:
            time_lesson = TimeRange(f"{lesson.time_lesson_start} - {lesson.time_lesson_end}")
            if time_lesson == tr:
                return True
    return False


def is_user_already_requested_lesson(day_date: datetime.date, tr: TimeRange, user: str) -> bool:
    user_lessons = Lesson.objects.filter(date_lesson=day_date, user=user)
    if user_lessons:
        for lesson in user_lessons:
            time_lesson = TimeRange(f"{lesson.time_lesson_start} - {lesson.time_lesson_end}")
            if time_lesson == tr:
                return True
    return False
