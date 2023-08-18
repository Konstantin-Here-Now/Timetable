from calendar import monthrange
from datetime import datetime, timedelta

from main.models import AvailableTimeModel


def get_actual_dates() -> dict[str, str]:
    dates = {}
    today = datetime.today()
    print(today)
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


def update_dates(actual_dates: dict[str, str] = None) -> None:
    actual_dates = get_actual_dates() if actual_dates is None else actual_dates
    AvailableTimeModel.objects.filter(time_type="dates").update(**actual_dates)


def get_dates_from_db() -> dict[str, str]:
    result = AvailableTimeModel.objects.filter(time_type='dates').values()[0]
    return result


def get_day_from_date(input_date: datetime.date) -> str:
    return input_date.strftime("%A").lower()


def is_date_in_db(input_date: datetime.date) -> bool:
    return input_date.strftime("%d.%m") in get_dates_from_db().values()
