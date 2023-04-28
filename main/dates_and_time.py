import json
from datetime import datetime, timedelta
from calendar import monthrange

TODAY = datetime.today()


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


def convert_min_into_str_time_ranges(day_at: list) -> str:
    time_list = []
    for at_time in day_at:
        time_list.append(min_to_time_range(at_time))
    day_at = ", ".join(time_list)

    return day_at


def inserting_into_right_place(time_range: tuple, time_interval: tuple) -> tuple:
    if (time_range[0] == time_interval[0]) and (time_range[1] == time_interval[1]):
        print('They are the same!')
        return 0,
    elif time_range[0] == time_interval[0]:
        print('Beginning is the same!')
        return time_range[1], time_interval[1]
    elif time_range[1] == time_interval[1]:
        print('End is the same!')
        return time_interval[0], time_range[0]
    else:
        print('Somewhere between!')
        return (time_interval[0], time_range[0]), (time_range[1], time_interval[1])


def clearing_nulls_in_available_time(at_time: list):
    print('Deleting zero intervals...')
    if len(at_time) > 1:
        for index, time_interval in enumerate(at_time):
            if time_interval == (0,):
                at_time = at_time[:index] + at_time[index + 1:]
    return at_time


def update_data():
    set_dates()
    update_today_time_to_default()


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


def update_today_time_to_default():
    print('<<Updating today time>>')
    with open('../main/dates_and_time.json', 'r+', encoding='UTF-8') as dates_f, \
            open('../main/available_time.json', 'r', encoding='UTF-8') as at_f:  # at_f = available time file
        days_data = json.loads(dates_f.read())
        at_data = json.loads(at_f.read())
        today_eng = TODAY.strftime('%A')
        days_data[today_eng]['available_time'] = at_data[today_eng]
        rewrite_json_file(days_data, dates_f)
    print('<<Update complete>>')


def set_dates():
    print('<<Setting dates>>')
    with open('../main/dates_and_time.json', 'r+', encoding='UTF-8') as dates_f:
        days_data = json.loads(dates_f.read())
        tomorrow = TODAY + timedelta(days=1)
        tomorrow_eng = tomorrow.strftime('%A')
        tomorrow_date = list(map(int, tomorrow.strftime("%d.%m").split('.')))
        days = tuple(days_data.keys())
        for index, day in enumerate(days):
            diff = days.index(tomorrow_eng) - index
            if diff > 0:
                diff -= 7
            day_date = str(tomorrow_date[0] - diff)

            # check if days_date exceeds month's number of days
            today_year_month = list(map(int, TODAY.strftime("%Y-%m").split('-')))
            number_of_days_in_month = monthrange(*today_year_month)[1]
            if int(day_date) > number_of_days_in_month:
                day_date = str(int(day_date) - number_of_days_in_month)

            if int(day_date) < 10:
                day_date = '0' + day_date
            month_date = str(tomorrow_date[1]) if tomorrow_date[1] > 9 else '0' + str(tomorrow_date[1])
            days_data[day]['date'] = '.'.join((day_date, month_date))
        rewrite_json_file(days_data, dates_f)
    print('<<Setting complete>>')


def change_time_interval(time_range: str, day: str):
    print(f'<<Setting new time interval for {day}...>>')
    with open('../main/dates_and_time.json', 'r+', encoding='UTF-8') as dates_f:
        days_data = json.loads(dates_f.read())
        day_at_data = days_data[day]['available_time']
        at_time = get_available_time_in_min(day_at_data)
        days_data[day]['available_time'] = insert_time_range(time_range, at_time)
        days_data[day]['available_time'] = convert_min_into_str_time_ranges(days_data[day]['available_time'])
        rewrite_json_file(days_data, dates_f)
    print('<<Setting complete>>')


def insert_time_range(time_range: str, at_time: list) -> list:
    if at_time == [(0,)]:
        print(f'---{time_range} ignored. No available time---')
    time_range = time_range_to_min(time_range)
    for index, time_interval in enumerate(at_time):
        if (time_interval[0] <= time_range[0]) and (time_interval[1] >= time_range[1]):
            new_at = inserting_into_right_place(time_range, time_interval)
            if type(new_at[0]) == int:
                at_time[index] = new_at
                print('---Changed---')
            else:
                at_time = at_time[:index] + [new_at[0], new_at[1]] + at_time[index + 1:]
                print('---Two new intervals---')
            return clearing_nulls_in_available_time(at_time)
    print(f'---{time_range} ignored. It exceeds available time---')


def rewrite_json_file(data, file):
    print('Rewriting json...')
    file.seek(0)
    file.truncate(0)
    json.dump(data, file, ensure_ascii=False, indent=4)


def time_range_to_min(time_range: str) -> tuple:
    tr_separated = list(map(str.strip, time_range.split('-')))
    for index, time in enumerate(tr_separated):
        time_list = list(map(int, time.split(':')))
        tr_separated[index] = time_list[0] * 60 + time_list[1]
    return tuple(tr_separated)


def get_available_time_in_min(day_at: str) -> list:
    print('Converting time string to mins list of tuples...')
    if len(day_at) == 13:
        day_at = [time_range_to_min(day_at)]
    elif len(day_at) > 13:
        at_time = list(map(str.strip, day_at.split(',')))
        for index in range(len(at_time)):
            at_time[index] = time_range_to_min(at_time[index])
        day_at = at_time
    else:
        day_at = [(0,)]

    return day_at

# change_time_inverval('15:00 - 18:00', 'Saturday')

# update_data()
