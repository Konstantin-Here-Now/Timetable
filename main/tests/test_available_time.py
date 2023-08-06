import pytest
from ..business_logic.available_time import AvailableTime
from ..business_logic.time_range import TimeRange

EXAMPLE_AVAILABLE_TIME = '12:00 - 13:00, 14:00 - 15:00'


@pytest.fixture
def test_class():
    test_class_example = AvailableTime(EXAMPLE_AVAILABLE_TIME)
    return test_class_example


class TestAvailableTime:
    def test_to_list_of_time_ranges_default(self, test_class):
        result = test_class._to_list_of_time_ranges('12:00 - 13:00, 14:00 - 15:00')
        assert result == [TimeRange("12:00 - 13:00"), TimeRange("14:00 - 15:00")]

    def test_to_list_of_time_ranges_error(self, test_class):
        with pytest.raises(ValueError) as err_info:
            test_class._to_list_of_time_ranges("sdf;sfllsf;")
        assert str(err_info.value) == "Time range should look like this: '00:00 - 00:00'"

    def test_at_str(self, test_class):
        result = test_class.at_str
        assert result == EXAMPLE_AVAILABLE_TIME
