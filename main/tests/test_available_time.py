import pytest
from ..business_logic.available_time import AvailableTime
from ..business_logic.exceptions import AvailableTimeExceeded
from ..business_logic.time_range import TimeRange

EXAMPLE_AVAILABLE_TIME = '12:00 - 13:00, 14:00 - 15:00'


@pytest.fixture
def test_class_at():
    test_class_example = AvailableTime(EXAMPLE_AVAILABLE_TIME)
    return test_class_example


class TestAvailableTime:
    def test_to_list_of_time_ranges_default(self, test_class_at):
        result = test_class_at._to_list_of_time_ranges('12:00 - 13:00, 14:00 - 15:00')
        assert result == [TimeRange("12:00 - 13:00"), TimeRange("14:00 - 15:00")]

    def test_to_list_of_time_ranges_error(self, test_class_at):
        with pytest.raises(ValueError) as err_info:
            test_class_at._to_list_of_time_ranges("sdf;sfllsf;")
        assert str(err_info.value) == "Time range should look like this: '00:00 - 00:00'"

    def test_at_str(self, test_class_at):
        result = test_class_at.at_str
        assert result == EXAMPLE_AVAILABLE_TIME

    def test_insert_same(self, test_class_at):
        test_class_at.insert(TimeRange("12:00 - 13:00"))
        assert test_class_at.at_str == '14:00 - 15:00'

    def test_insert_left(self, test_class_at):
        test_class_at.insert(TimeRange("12:00 - 12:30"))
        assert test_class_at.at_str == '12:30 - 13:00, 14:00 - 15:00'

    def test_insert_right(self, test_class_at):
        test_class_at.insert(TimeRange("14:30 - 15:00"))
        assert test_class_at.at_str == '12:00 - 13:00, 14:00 - 14:30'

    def test_insert_between(self, test_class_at):
        test_class_at.insert(TimeRange("12:30 - 12:40"))
        assert test_class_at.at_str == '12:00 - 12:30, 12:40 - 13:00, 14:00 - 15:00'

    def test_insert_error_case_no_at(self, test_class_at):
        test_class_at.at = []
        with pytest.raises(AvailableTimeExceeded) as err_info:
            test_class_at.insert(TimeRange("10:00 - 11:00"))
        assert str(err_info.value) == "No time available"

    def test_insert_error_case_1(self, test_class_at):
        with pytest.raises(AvailableTimeExceeded) as err_info:
            test_class_at.insert(TimeRange("10:00 - 11:00"))
        assert str(err_info.value) == "Available time exceeded"

    def test_insert_error_case_2(self, test_class_at):
        with pytest.raises(AvailableTimeExceeded) as err_info:
            test_class_at.insert(TimeRange("13:30 - 13:40"))
        assert str(err_info.value) == "Available time exceeded"

    def test_insert_error_case_3(self, test_class_at):
        with pytest.raises(AvailableTimeExceeded) as err_info:
            test_class_at.insert(TimeRange("14:00 - 16:00"))
        assert str(err_info.value) == "End is further"

    def test_insert_error_case_4(self, test_class_at):
        with pytest.raises(AvailableTimeExceeded) as err_info:
            test_class_at.insert(TimeRange("11:00 - 13:00"))
        assert str(err_info.value) == "Start is earlier"
