from django.conf import settings

from main.business_logic.dates_controller import get_actual_dates
from main.models import AvailableTimeModel


def create_time_tables(at_data: dict[str, str] = settings.AVAILABLE_TIME) -> None:
    AvailableTimeModel.objects.create(time_type='default', **at_data)
    AvailableTimeModel.objects.create(time_type='actual', **at_data)
    AvailableTimeModel.objects.create(time_type='dates', **get_actual_dates())
