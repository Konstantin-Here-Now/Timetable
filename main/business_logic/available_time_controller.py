import os
from typing import Literal

import yaml
from django.conf import settings

from main.business_logic.available_time import AvailableTime
from main.models import AvailableTimeModel

with open(os.path.join(settings.BASE_DIR, r'config.yaml'), 'r') as data_f:
    CONFIGURED_AVAILABLE_TIME = yaml.load(data_f, yaml.BaseLoader)['default_available_time']


def set_default_time(at_data: dict[str, str] = CONFIGURED_AVAILABLE_TIME) -> None:
    AvailableTimeModel.objects.filter(time_type="default").update(**at_data)


def reset_actual_at_to_default() -> None:
    AvailableTimeModel.objects.filter(time_type="actual").update(**CONFIGURED_AVAILABLE_TIME)


def set_day_available_time(day: str, available_time: AvailableTime) -> None:
    new_at = {day: str(available_time)}
    AvailableTimeModel.objects.filter(time_type="actual").update(**new_at)


def get_available_time(time_type: Literal["default", "actual"]) -> dict[str, str]:
    result = AvailableTimeModel.objects.filter(time_type=time_type).values()[0]
    return result
