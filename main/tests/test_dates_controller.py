import datetime
import pytest
import re
from main.business_logic.dates_controller import get_actual_dates, update_dates, get_dates_from_db
from main.db_connection import create_dates_table

FAKE_TIME = datetime.datetime(year=2023, month=12, day=25, hour=17, minute=5, second=55)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class MockDatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)


class TestGetActualDates:
    def test_should_be_no_today_date(self):
        today_date = datetime.datetime.today().strftime("%d.%m")
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

    def test_patch_datetime(self, patch_datetime_now):
        result = get_actual_dates()
        expected_dates_dict = {'friday': '18.08',
                               'monday': '14.08',
                               'saturday': '12.08',
                               'sunday': '13.08',
                               'thursday': '17.08',
                               'tuesday': '15.08',
                               'wednesday': '16.08'}
        assert result == expected_dates_dict


class TestOperationsWithDB:
    @pytest.mark.django_db(transaction=True)
    def test_update_dates(self):
        create_dates_table()

        mock_dates = {'friday': '18.08',
                      'monday': '14.08',
                      'saturday': '12.08',
                      'sunday': '13.08',
                      'thursday': '17.08',
                      'tuesday': '15.08',
                      'wednesday': '16.08'}
        update_dates(mock_dates)
        result = get_dates_from_db()
        del result['time_type']
        assert result == mock_dates

    @pytest.mark.django_db(transaction=True)
    def test_get_dates_from_db(self):
        pass

