import json
from datetime import datetime

AVAILABLE_TIME = {'Monday': '17:00 - 19:00',
                  'Tuesday': '19:00 - 23:00',
                  'Wednesday': '---',
                  'Thursday': '17:00 - 23:00',
                  'Friday': '---',
                  'Saturday': '09:00 - 11:00, 14:00 - 23:00',
                  'Sunday': '---'}


class TimeRangeNotInAvailableTime(Exception):
    def __str__(self):
        return "Временной интервал не доступен среди свободного времени."


def update_data():
    set_dates()
    pass


def set_general_available_time():
    print('<<Setting available time>>')
    with open('../main/dates_and_time.json', 'r+', encoding='UTF-8') as dates_f, \
            open('../main/available_time.json', 'r', encoding='UTF-8') as at_f:  # at_f = available time file
        days_data = json.loads(dates_f.read())
        at_data = json.loads(at_f.read())
        for day in days_data.keys():
            days_data[day]['available_time'] = at_data[day]
        rewrite_json_file(days_data, dates_f)
    print('<<Setting complete>>')


def set_dates():
    print('<<Setting dates>>')
    with open('../main/dates_and_time.json', 'r+', encoding='UTF-8') as dates_f:
        days_data = json.loads(dates_f.read())
        today_eng = datetime.today().strftime('%A')
        today_date = list(map(int, datetime.today().strftime("%d.%m").split('.')))
        days = tuple(days_data.keys())
        for index, day in enumerate(days):
            diff = days.index(today_eng) - index
            if diff > 0:
                diff -= 7
            day_date = str(today_date[0] - diff)
            month_date = str(today_date[1]) if today_date[1] > 9 else '0' + str(today_date[1])
            days_data[day]['date'] = '.'.join((day_date, month_date))
        rewrite_json_file(days_data, dates_f)
    print('<<Setting complete>>')


def rewrite_json_file(data, file):
    print('Rewriting json...')
    file.seek(0)
    file.truncate(0)
    json.dump(data, file, ensure_ascii=False, indent=4)


def get_available_time_in_min(days_data: dict):
    for day in days_data:
        if len(days_data[day]) == 13:
            days_data[day] = [time_range_to_min(days_data[day])]
        elif len(days_data[day]) > 13:
            at_time = list(map(str.strip, days_data[day].split(',')))
            for index in range(len(at_time)):
                at_time[index] = time_range_to_min(at_time[index])
            days_data[day] = at_time
        else:
            days_data[day] = [(0,)]

    return days_data
    # for day in self.data.keys():
    #     self.data[day]['available_time'] = days_data[day]


def time_range_to_min(time_range: str) -> tuple:
    tr_separated = list(map(str.strip, time_range.split('-')))
    for index, time in enumerate(tr_separated):
        time_list = list(map(int, time.split(':')))
        tr_separated[index] = time_list[0] * 60 + time_list[1]
    return tuple(tr_separated)


def min_to_real_time(minutes: int) -> str:
    hours = minutes // 60
    if hours < 10:
        hours = f'0{hours}'
    minutes = minutes % 60
    if minutes % 10 == 0:
        minutes = f'{minutes}0'
    return f'{hours}:{minutes}'


def min_to_time_range(time_range_min: tuple) -> str:
    if time_range_min == (0,):
        return '---'
    range_start = min_to_real_time(time_range_min[0])
    range_end = min_to_real_time(time_range_min[1])
    return f'{range_start} - {range_end}'


def convert_min_into_str_time_ranges(days_data: dict) -> dict:
    for day in days_data:
        time_list = []
        for at_time in days_data[day]['available_time']:
            time_list.append(min_to_time_range(at_time))
        days_data[day]['available_time'] = ", ".join(time_list)
    return days_data


class DaysData:
    def __init__(self):
        self.data = dict()
        self.data = get_available_time_in_min(AVAILABLE_TIME)
        pass

    def insert_time_range(self, time_range: str, at_time: list):
        if at_time == [(0,)]:
            raise TimeRangeNotInAvailableTime
        time_range = time_range_to_min(time_range)
        for index, time_interval in enumerate(at_time):
            if (time_interval[0] <= time_range[0]) and (time_interval[1] >= time_range[1]):
                new_at = self.inserting_into_right_place(time_range, time_interval)
                if type(new_at[0]) == int:
                    print('CHANGED')
                    at_time[index] = new_at
                else:
                    print('TWO NEW INTERVALS')
                    at_time = at_time[:index] + [new_at[0], new_at[1]] + at_time[index + 1:]
                return self.clearing_nulls_in_available_time(at_time)
        raise TimeRangeNotInAvailableTime

    @staticmethod
    def inserting_into_right_place(time_range: tuple, time_interval: tuple) -> tuple:
        if (time_range[0] == time_interval[0]) and (time_range[1] == time_interval[1]):
            print('They are the same')
            return 0,
        elif time_range[0] == time_interval[0]:
            print('Beginning is the same')
            return time_range[1], time_interval[1]
        elif time_range[1] == time_interval[1]:
            print('End is the same')
            return time_interval[0], time_range[0]
        else:
            print('Somewhere between')
            return (time_interval[0], time_range[0]), (time_range[1], time_interval[1])

    @staticmethod
    def clearing_nulls_in_available_time(at_time: list):
        if len(at_time) > 1:
            for index, time_interval in enumerate(at_time):
                if time_interval == (0,):
                    at_time = at_time[:index] + at_time[index + 1:]
        return at_time
