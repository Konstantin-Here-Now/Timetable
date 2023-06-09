import json
import logging
import os
import sqlite3
from calendar import monthrange
from datetime import datetime, timedelta

from django.conf import settings

logger = logging.getLogger(__name__)

TODAY = datetime.today()
DATES_JSON_PATH = os.path.join(settings.BASE_DIR, r'main/dates_and_time.json')
AT_PATH = os.path.join(settings.BASE_DIR, r'main/available_time.json')


def min_to_real_time(minutes: int) -> str:
    hours = minutes // 60
    if hours < 10:
        hours = f'0{hours}'
    minutes = minutes % 60
    if minutes < 10:
        minutes = f'0{minutes}'
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


def inserting_into_right_place(time_range_to_insert: tuple, at_time_interval: tuple) -> tuple:
    if time_range_to_insert[0] < at_time_interval[0] or time_range_to_insert[1] > at_time_interval[1]:
        raise ValueError("Time range exceeded.")
    if (time_range_to_insert[0] == at_time_interval[0]) and (time_range_to_insert[1] == at_time_interval[1]):
        logger.info('They are the same!')
        return 0,
    elif time_range_to_insert[0] == at_time_interval[0]:
        logger.info('Beginning is the same!')
        return time_range_to_insert[1], at_time_interval[1]
    elif time_range_to_insert[1] == at_time_interval[1]:
        logger.info('End is the same!')
        return at_time_interval[0], time_range_to_insert[0]
    else:
        logger.info('Somewhere between!')
        return (at_time_interval[0], time_range_to_insert[0]), (time_range_to_insert[1], at_time_interval[1])


def clearing_nulls_in_available_time(at_time: list) -> list:
    logger.info('Deleting zero intervals...')
    if len(at_time) > 1:
        at_time = [time_range for time_range in at_time if time_range != (0,)]
    return at_time


def set_general_available_time():
    logger.info('<<Setting available time>>')
    with open(DATES_JSON_PATH, 'r+', encoding='UTF-8') as dates_f, \
            open(AT_PATH, 'r', encoding='UTF-8') as at_f:  # at_f = available time file
        days_data = json.loads(dates_f.read())
        at_data = json.loads(at_f.read())
        for day in days_data.keys():
            days_data[day]['available_time'] = at_data[day]
        rewrite_json_file(days_data, dates_f)
    logger.info('<<Setting complete>>')


def set_dates():
    logger.info('<<Setting dates>>')
    with open(DATES_JSON_PATH, 'r+', encoding='UTF-8') as dates_f:
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

            # check if it's end of the month (then increment month number)
            if int(day_date) == number_of_days_in_month:
                tomorrow_date[1] += 1
        rewrite_json_file(days_data, dates_f)
    logger.info('<<Setting complete>>')


def change_time_interval(time_range: str, day: str):
    logger.info(f'<<Setting new time interval for {day}...>>')
    with open(DATES_JSON_PATH, 'r+', encoding='UTF-8') as dates_f:
        days_data = json.loads(dates_f.read())
        day_at_data = days_data[day]['available_time']
        at_time = get_available_time_in_min(day_at_data)
        days_data[day]['available_time'] = insert_time_range(time_range, at_time)
        days_data[day]['available_time'] = convert_min_into_str_time_ranges(days_data[day]['available_time'])
        rewrite_json_file(days_data, dates_f)
    logger.info('<<Setting complete>>')


def insert_time_range(time_range: str, at_time: list) -> list:
    logger.info('Inserting time range...')
    if at_time == [(0,)]:
        logger.info(f'---{time_range} ignored. No available time---')
        return at_time
    time_range = time_range_to_min(time_range)
    for index, time_interval in enumerate(at_time):
        if (time_interval[0] <= time_range[0]) and (time_interval[1] >= time_range[1]):
            new_at = inserting_into_right_place(time_range, time_interval)
            if type(new_at[0]) == int:
                at_time[index] = new_at
                logger.info('---Changed---')
            else:
                at_time = at_time[:index] + [new_at[0], new_at[1]] + at_time[index + 1:]
                logger.info('---Two new intervals---')
            return clearing_nulls_in_available_time(at_time)
    logger.info(f'---{time_range} ignored. It exceeds available time---')
    return at_time


def rewrite_json_file(data, file):
    logger.info('Rewriting json...')
    file.seek(0)
    file.truncate(0)
    json.dump(data, file, ensure_ascii=False, indent=4)
    logger.info('Rewriting done')


def time_range_to_min(time_range: str) -> tuple:
    try:
        tr_separated = list(map(str.strip, time_range.split('-')))
        for index, time in enumerate(tr_separated):
            time_list = list(map(int, time.split(':')))
            tr_separated[index] = time_list[0] * 60 + time_list[1]
        return tuple(tr_separated) if tr_separated != [0, 0] else (0,)
    except ValueError:
        raise ValueError("Time range should be like this: '12:00 - 13:00'")


def get_available_time_in_min(day_at: str) -> list:
    logger.info('Converting time string to mins list of tuples...')
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


def update():
    logger.info('<<Updating available time intervals>>')
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    day_after_7_days = TODAY + timedelta(days=7)
    cur = conn.cursor()
    cur.execute(
        f"""SELECT * from main_lesson 
        WHERE date_lesson >= '{TODAY.date()}' AND approved = TRUE AND date_lesson < '{day_after_7_days.date()}'""")
    result = cur.fetchall()
    conn.close()

    set_general_available_time()
    set_dates()

    lessons_data_dict = dict()
    for element in result:
        lesson_time = f'{element[2][:-3]} - {element[3][:-3]}'
        lesson_date = '.'.join(element[1].split('-')[-1:-3:-1])
        lessons_data_dict[lesson_date] = lesson_time

    with open(DATES_JSON_PATH, 'r+', encoding='UTF-8') as dates_f:
        days_data = json.loads(dates_f.read())
        for day in days_data:
            if days_data[day]['date'] in lessons_data_dict:
                days_data[day]['available_time'] = insert_time_range(lessons_data_dict[days_data[day]['date']],
                                                                     get_available_time_in_min(
                                                                         days_data[day]['available_time']))
                days_data[day]['available_time'] = convert_min_into_str_time_ranges(days_data[day]['available_time'])
        rewrite_json_file(days_data, dates_f)
    logger.info('<<Update complete>>')
