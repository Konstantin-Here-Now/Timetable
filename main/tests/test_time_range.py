import pytest
from ..business_logic.time_range import TimeRange

EXAMPLE_TIME_RANGE = '12:00 - 18:00'


@pytest.fixture
def test_class_tr():
    test_class_example = TimeRange(EXAMPLE_TIME_RANGE)
    return test_class_example


class TestTimeRange:
    def test_to_tuple_of_minutes_default(self, test_class_tr):
        result = test_class_tr.to_tuple_of_minutes(EXAMPLE_TIME_RANGE)
        assert result == (720, 1080)

    def test_to_tuple_of_minutes_error(self, test_class_tr):
        with pytest.raises(ValueError) as err_info:
            test_class_tr.to_tuple_of_minutes("0:0 - 0:0")
        assert str(err_info.value) == "Time range should look like this: '00:00 - 00:00'"

    def test_check_time_order_default(self, test_class_tr):
        test_time_range_in_min = (700, 900)
        result = test_class_tr._check_time_order(test_time_range_in_min)
        assert result == test_time_range_in_min

    def test_check_time_order_midnight_at_the_end(self, test_class_tr):
        test_time_range_in_min = (700, 0)
        result = test_class_tr._check_time_order(test_time_range_in_min)
        assert result == (700, 1440)

    def test_check_time_order_error_end_earlier(self, test_class_tr):
        with pytest.raises(ValueError) as err_info:
            test_class_tr._check_time_order((700, 100))
        assert str(err_info.value) == "End is earlier beginning!"

    def test_check_time_order_error_end_same_as_beginning(self, test_class_tr):
        with pytest.raises(ValueError) as err_info:
            test_class_tr._check_time_order((700, 700))
        assert str(err_info.value) == "End is the same as beginning!"

    def test_time_range_str_output(self, test_class_tr):
        assert str(test_class_tr) == EXAMPLE_TIME_RANGE
