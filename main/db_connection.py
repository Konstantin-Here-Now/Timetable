from typing import Literal
from django.conf import settings
from main.models import AvailableTimeModel
from main.business_logic.available_time import AvailableTime
from main.business_logic.update_time import get_dates


def create_time_tables(at_data: dict[str, str] = settings.AVAILABLE_TIME) -> None:
    # AvailableTimeModel.objects.create(time_type='default', **at_data)
    # AvailableTimeModel.objects.create(time_type='actual', **at_data)
    AvailableTimeModel.objects.create(time_type='dates', **get_dates())


def get_available_time(time_type: Literal["default", "actual"]) -> dict[str, str]:
    result = AvailableTimeModel.objects.filter(time_type=time_type).values()[0]
    return result


def set_default_time(at_data: dict[str, str] = settings.AVAILABLE_TIME) -> None:
    AvailableTimeModel.objects.filter(time_type="default").update(**at_data)


def set_day_available_time(day: str, available_time: AvailableTime) -> None:
    new_at = {day: str(available_time)}
    AvailableTimeModel.objects.filter(time_type="actual").update(**new_at)


def update_dates(actual_dates: dict[str, str] = None) -> None:
    actual_dates = get_dates() if actual_dates is None else actual_dates
    AvailableTimeModel.objects.filter(time_type="dates").update(**actual_dates)


def get_actual_dates() -> dict[str, str]:
    result = AvailableTimeModel.objects.filter(time_type='dates').values()[0]
    return result
