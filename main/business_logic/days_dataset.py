from main.business_logic.available_time_controller import get_available_time
from main.business_logic.dates_controller import get_actual_dates


def get_days_dataset() -> dict[str, dict[str, str]]:
    available_time = get_available_time(time_type="actual")
    dates = get_actual_dates()
    rus_names: dict[str, str] = {
        'monday': "Понедельник",
        'tuesday': "Вторник",
        'wednesday': "Среда",
        'thursday': "Четверг",
        'friday': "Пятница",
        'saturday': "Суббота",
        'sunday': "Воскресенье"
    }

    days_dataset = {}
    for day in dates:
        days_dataset[day] = {"date": '', "rus": '', "available_time": ''}
        days_dataset[day]["date"] = dates[day]
        days_dataset[day]["rus"] = rus_names[day]
        days_dataset[day]["available_time"] = available_time[day]
    return days_dataset
