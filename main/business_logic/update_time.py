import datetime

from main.business_logic.available_time import AvailableTime
from main.business_logic.available_time_controller import get_available_time, set_day_available_time
from main.business_logic.dates_controller import is_date_in_db, get_day_from_date, get_actual_dates
from main.business_logic.exceptions import AvailableTimeExceeded
from main.business_logic.time_range import TimeRange


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
    actual_dates = get_actual_dates()
    actual_lessons = ...
    # make update for every lesson
    pass
