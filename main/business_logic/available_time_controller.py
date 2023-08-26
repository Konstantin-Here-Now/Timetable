import logging
import os
from typing import Literal

import yaml
from django.conf import settings

from main.business_logic.available_time import AvailableTime
from main.models import AvailableTimeModel

logger = logging.getLogger(__name__)

with open(os.path.join(settings.BASE_DIR, r'config.yaml'), 'r') as data_f:
    CONFIGURED_AVAILABLE_TIME = yaml.load(data_f, yaml.BaseLoader)['default_available_time']


def set_default_time(at_data: dict[str, str] = CONFIGURED_AVAILABLE_TIME) -> None:
    logger.info('Setting new default available time...')
    AvailableTimeModel.objects.filter(time_type="default").update(**at_data)
    logger.info('New default available time has been set.')


def reset_actual_at_to_default() -> None:
    logger.info('Resetting to default available time...')
    AvailableTimeModel.objects.filter(time_type="actual").update(**CONFIGURED_AVAILABLE_TIME)
    logger.info('Available time has been reset to default.')


def set_day_available_time(day: str, available_time: AvailableTime) -> None:
    logger.info("Setting new days' available time...")
    new_at = {day: str(available_time)}
    AvailableTimeModel.objects.filter(time_type="actual").update(**new_at)
    logger.info("New days' available time has been set.")


def get_available_time(time_type: Literal["default", "actual"]) -> dict[str, str]:
    result = AvailableTimeModel.objects.filter(time_type=time_type).values()[0]
    return result
