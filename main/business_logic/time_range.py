from datetime import time

# examples: "00:00 - 00:00", "12:00 - 13:00"
TIME_RANGE_PATTERN = r'\d{2}:\d{2} - \d{2}:\d{2}'


class TimeRange:
    def __init__(self, time_range: str | tuple[int, int]):
        time_range_in_minutes = self._to_tuple_of_minutes(time_range) if isinstance(time_range, str) else time_range
        proper_time_range = self._check_time_order(time_range_in_minutes)

        self.time_range_in_min: tuple[int, int] = proper_time_range

    def __str__(self):
        time_range_start_str = '{:02d}:{:02d}'.format(*divmod(self.start, 60))
        time_range_end_str = '{:02d}:{:02d}'.format(*divmod(self.end, 60))

        return f'{time_range_start_str} - {time_range_end_str}'

    def __repr__(self):
        return f"TimeRange({self.time_range_in_min})"

    def __eq__(self, other):
        if isinstance(other, TimeRange):
            return self.time_range_in_min == other.time_range_in_min
        return False

    @property
    def start(self):
        return self.time_range_in_min[0]

    @property
    def end(self):
        return self.time_range_in_min[1]

    @staticmethod
    def _check_time_order(time_range: tuple[int, int]) -> tuple[int, int] | ValueError:
        time_range_start = time_range[0]
        time_range_end = time_range[1] if time_range[1] != 0 else 1440
        if time_range_end > time_range_start:
            return time_range_start, time_range_end
        elif time_range_start == time_range_end:
            raise ValueError("End is the same as beginning!")
        else:
            raise ValueError("End is earlier beginning!")

    @staticmethod
    def _to_tuple_of_minutes(time_range: TIME_RANGE_PATTERN) -> tuple[int, int] | ValueError:
        try:
            time_range_separated = list(map(str.strip, time_range.split('-')))
            output_time_range = [0, 0]
            for index, hour_minute in enumerate(time_range_separated):
                time_element = time.fromisoformat(hour_minute)
                output_time_range[index] = time_element.hour * 60 + time_element.minute
            return output_time_range[0], output_time_range[1]
        except ValueError:
            raise ValueError("Time range should look like this: '00:00 - 00:00'")
