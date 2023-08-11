import datetime

from main.business_logic.available_time import AvailableTime
from main.business_logic.available_time_controller import get_available_time, set_day_available_time, set_default_time, \
    reset_actual_at_to_default
from main.business_logic.dates_controller import is_date_in_db, get_day_from_date, get_actual_dates, update_dates
from main.business_logic.exceptions import AvailableTimeExceeded
from main.business_logic.time_range import TimeRange
from main.business_logic.lessons_getter import get_actual_lessons


def update(input_date: datetime.date, new_tr: TimeRange) -> None:
    if not is_date_in_db(input_date):
        return None
    else:
        day = get_day_from_date(input_date)
        available_time = AvailableTime(get_available_time(time_type="actual")[day])
        try:
            available_time.insert(new_tr)
        except AvailableTimeExceeded as err:
            # logger
            print(f'Insertion ignored. Error message (reason): "{err}"')
        set_day_available_time(day, available_time)


def daily_update():
    reset_actual_at_to_default()
    update_dates()

    actual_dates = get_actual_dates().values()
    actual_lessons = get_actual_lessons()
    for lesson in actual_lessons:
        date_lesson = lesson["date_lesson"]
        time_lesson = f"{lesson['time_lesson_start']} - {lesson['time_lesson_end']}"
        if date_lesson.strftime("%d.%m") in actual_dates and lesson['approved'] is True:
            update(date_lesson, TimeRange(time_lesson))
