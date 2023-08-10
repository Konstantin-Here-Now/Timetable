from calendar import monthrange
from datetime import datetime, timedelta


def get_dates() -> dict[str, str]:
    dates = {}
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    tomorrow_eng = tomorrow.strftime('%A').lower()
    tomorrow_date = list(map(int, tomorrow.strftime("%d.%m").split('.')))

    days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    for index, day in enumerate(days):
        diff = days.index(tomorrow_eng) - index
        if diff > 0:
            diff -= 7
        day_date = str(tomorrow_date[0] - diff)

        # check if days_date exceeds month's number of days
        today_year_month = list(map(int, today.strftime("%Y-%m").split('-')))
        number_of_days_in_month = monthrange(*today_year_month)[1]
        if int(day_date) > number_of_days_in_month:
            day_date = str(int(day_date) - number_of_days_in_month)

        if int(day_date) < 10:
            day_date = '0' + day_date
        month_date = str(tomorrow_date[1]) if tomorrow_date[1] > 9 else '0' + str(tomorrow_date[1])
        dates[day] = '.'.join((day_date, month_date))

        # check if it's end of the month (then increment month number)
        if int(day_date) == number_of_days_in_month:
            tomorrow_date[1] += 1
    return dates


# TODO is_time_available
# def is_time_available(day_date: date, time_range: str) -> bool:
#     logger.info('Check if time available...')
#     day_name = day_date.strftime('%A')
#     if day_date > (TODAY + timedelta(days=7)).date():
#         with open(AT_PATH, 'r', encoding='UTF-8') as at_f:
#             at_data = json.loads(at_f.read())
#     else:
#         with open(DATES_JSON_PATH, 'r+', encoding='UTF-8') as dates_f:
#             at_data = json.loads(dates_f.read())
#     before_adding_new_time_range = get_available_time_in_min(at_data[day_name]['available_time'])
#     after_adding_new_time_range = insert_time_range(time_range, before_adding_new_time_range)
#     return not before_adding_new_time_range == after_adding_new_time_range
