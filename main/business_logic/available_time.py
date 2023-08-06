from typing import Iterable

from main.business_logic.time_range import TimeRange


class AvailableTime:
    def __init__(self, at: str):
        self.at: Iterable[TimeRange] = self._to_list_of_time_ranges(at)

    @staticmethod
    def _to_list_of_time_ranges(available_time: str) -> Iterable[TimeRange]:
        available_time_separated = list(map(str.strip, available_time.split(',')))
        if available_time_separated != ['']:
            for index in range(len(available_time_separated)):
                available_time_separated[index] = TimeRange(available_time_separated[index])
            return available_time_separated
        else:
            return []

    @property
    def at_str(self) -> str:
        list_of_at = [tr.time_range for tr in self.at]
        return ", ".join(list_of_at)


example = AvailableTime('12:00 - 13:00, 14:00 - 15:00')
for time_range in example.at:
    print(time_range.time_range)
    print(time_range == TimeRange('12:00 - 13:00'))

print(TimeRange('12:00 - 13:00'))
