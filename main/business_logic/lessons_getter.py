import datetime
from typing import Iterable

from main.models import Lesson


def get_actual_lessons() -> Iterable[dict]:
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=7)
    return Lesson.objects.filter(date_lesson__range=(start_date, end_date)).values()
