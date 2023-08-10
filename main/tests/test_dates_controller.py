import re
from datetime import datetime

from main.business_logic.dates_controller import get_actual_dates


class TestGetActualDates:
    def test_should_be_no_today_date(self):
        today_date = datetime.today().strftime("%d.%m")
        assert today_date not in get_actual_dates().values()

    def test_correct_keys(self):
        days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        dates = get_actual_dates()
        for day in days:
            assert day in dates

    def test_correct_dates(self):
        dates = get_actual_dates()
        for one_date in dates.values():
            assert bool(re.search(r'\d{1,2}\.\d{2}', one_date))
