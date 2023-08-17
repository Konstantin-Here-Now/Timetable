import datetime
from unittest.mock import Mock, patch

from django_mock_queries.query import MockSet, MockModel

import main.business_logic.time_controller as time_controller
from main.business_logic.time_range import TimeRange

MOCK_DEFAULT_AVAILABLE_TIME = {
    'monday': "17:00 - 19:00",
    'tuesday': "19:00 - 23:00",
    'wednesday': "---",
    'thursday': "17:00 - 23:00",
    'friday': "---",
    'saturday': "09:00 - 11:00, 14:00 - 23:00",
    'sunday': "10:00 - 11:00"
}

MOCK_LESSONS = MockSet(
    MockModel(date_lesson=datetime.date(2023, 8, 17),
              time_lesson_start=datetime.time(12, 0),
              time_lesson_end=datetime.time(13, 0)),
    MockModel(date_lesson=datetime.date(2023, 8, 17),
              time_lesson_start=datetime.time(15, 0),
              time_lesson_end=datetime.time(16, 0))
)


@patch("main.business_logic.time_controller.get_available_time", Mock(return_value=MOCK_DEFAULT_AVAILABLE_TIME))
def test_is_correspond_to_default_at_true():
    result = time_controller._is_correspond_to_default_at("monday", TimeRange("18:00 - 19:00"))
    assert result is True


@patch("main.business_logic.time_controller.get_available_time", Mock(return_value=MOCK_DEFAULT_AVAILABLE_TIME))
def test_is_correspond_to_default_at_false():
    result = time_controller._is_correspond_to_default_at("monday", TimeRange("23:00 - 00:00"))
    assert result is False


@patch("main.business_logic.time_controller.Lesson.objects", MOCK_LESSONS)
def test_is_already_occupied_true():
    mock_date = datetime.date(2023, 8, 17)
    result = time_controller._is_already_occupied(mock_date, TimeRange("12:00 - 13:00"))
    assert result is True


@patch("main.business_logic.time_controller.Lesson.objects", MOCK_LESSONS)
def test_is_already_occupied_false():
    mock_date = datetime.date(2023, 8, 17)
    result = time_controller._is_already_occupied(mock_date, TimeRange("18:00 - 19:00"))
    assert result is False
