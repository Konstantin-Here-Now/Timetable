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
