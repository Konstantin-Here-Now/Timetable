import pytest
from ..business_logic.time_range import TimeRange

EXAMPLE_TIME_RANGE = '12:00 - 18:00'


@pytest.fixture
def test_class():
    test_class_example = TimeRange(EXAMPLE_TIME_RANGE)
    return test_class_example


class TestTimeRange:
    def test_to_tuple_of_minutes_default(self, test_class):
        result = test_class._to_tuple_of_minutes(EXAMPLE_TIME_RANGE)
        assert result == (720, 1080)

    def test_to_tuple_of_minutes_error(self, test_class):
        with pytest.raises(ValueError) as err_info:
            test_class._to_tuple_of_minutes("0:0 - 0:0")
        assert str(err_info.value) == "Time range should look like this: '00:00 - 00:00'"

    def test_check_time_order_default(self):
        pass

    def test_check_time_order_error(self):
        pass

    def test_time_range_str_output(self, test_class):
        result = test_class.time_range
        assert result == EXAMPLE_TIME_RANGE
