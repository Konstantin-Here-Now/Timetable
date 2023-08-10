from main.business_logic.exceptions import AvailableTimeExceeded
from main.business_logic.time_range import TimeRange


# TODO at_str replace with __str__
class AvailableTime:
    def __init__(self, at: str):
        self.at: list[TimeRange] = self._to_list_of_time_ranges(at)

    def __str__(self):
        if self.at:
            list_of_at = [str(tr) for tr in self.at]
            return ", ".join(list_of_at)
        else:
            return "---"

    def __eq__(self, other):
        if isinstance(other, AvailableTime):
            return self.at == other.at
        return False

    # @property
    # def at_str(self) -> str:
    #     if self.at:
    #         list_of_at = [str(tr) for tr in self.at]
    #         return ", ".join(list_of_at)
    #     else:
    #         return "---"

    @staticmethod
    def _to_list_of_time_ranges(available_time: str) -> list[TimeRange]:
        available_time_separated = list(map(str.strip, available_time.split(',')))
        if available_time_separated != ['']:
            for index in range(len(available_time_separated)):
                available_time_separated[index] = TimeRange(available_time_separated[index])
            return available_time_separated
        else:
            return []

    def insert(self, tr_to_insert: TimeRange) -> None:
        if not self.at:
            raise AvailableTimeExceeded("No time available")
        else:
            is_at_changed = False
        for index, at_tr in enumerate(self.at):
            if is_at_changed:
                break
            else:
                is_at_changed = self._is_insert_successful(at_tr, tr_to_insert, index)
        if not is_at_changed:
            raise AvailableTimeExceeded("Available time exceeded")

    def _is_insert_successful(self, at_tr: TimeRange, tr_to_insert: TimeRange, index: int) -> bool:
        if at_tr.start == tr_to_insert.start and at_tr.end == tr_to_insert.end:
            self._same_interval_insert(index)
            return True
        elif at_tr.start == tr_to_insert.start:
            self._same_beginning_insert(at_tr, tr_to_insert, index)
            return True
        elif at_tr.end == tr_to_insert.end:
            self._same_end_insert(at_tr, tr_to_insert, index)
            return True
        elif at_tr.start < tr_to_insert.start and at_tr.end > tr_to_insert.end:
            self._between_insert(at_tr, tr_to_insert, index)
            return True

    def _same_interval_insert(self, index: int) -> None:
        at_list_before_index = self.at[:index]
        at_list_after_index = self.at[index + 1:]
        self.at = at_list_before_index + at_list_after_index

    def _same_beginning_insert(self, at_tr: TimeRange, tr_to_insert: TimeRange, index: int) -> None:
        if at_tr.end < tr_to_insert.end:
            raise AvailableTimeExceeded("End is further")
        else:
            changed_time_range = tr_to_insert.end, at_tr.end
            self.at[index] = TimeRange(changed_time_range)

    def _same_end_insert(self, at_tr: TimeRange, tr_to_insert: TimeRange, index: int) -> None:
        if at_tr.start > tr_to_insert.start:
            raise AvailableTimeExceeded("Start is earlier")
        else:
            changed_time_range = at_tr.start, tr_to_insert.start
            self.at[index] = TimeRange(changed_time_range)

    def _between_insert(self, at_tr: TimeRange, tr_to_insert: TimeRange, index: int) -> None:
        at_list_before_index = self.at[:index]
        at_list_after_index = self.at[index + 1:]
        new_tr_1 = TimeRange((at_tr.start, tr_to_insert.start))
        new_tr_2 = TimeRange((tr_to_insert.end, at_tr.end))
        self.at = at_list_before_index + [new_tr_1, new_tr_2] + at_list_after_index
