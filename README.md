# Timetable

Web app for enrolling in private lessons.

## Contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Technologies](#technologies)
- [File structure](#file-structure)
- [Testing](#testing)

## Requirements

To use the project, you need to install [Python 3](https://www.python.org/downloads/) (version 3.10 recommended) and
[Redis](https://redis.io/docs/getting-started/).

Other requirements should be installed via `configure` bash script (check [Quick start](#quick-start)).

## Quick start

### Installing virtual environment and libraries

Create virtual environment using bash console:

```bash
python3 -m venv YOUR_VIRTUAL_ENV_NAME
```

Activate virtual environment:

```bash
# Linux
source YOUR_VIRTUAL_ENV_NAME/bin/activate
# Windows
YOUR_VIRTUAL_ENV_NAME/Scripts/activate
```

**Execute** bash script `configure` (fullpath: `timetable/scripts/configure`).
It will create `logs/` folder, downgrade `setuptools` (necessary for `django-celery` library)
and install all the requirements. Moreover, it will proceed migrations to database and collect static files.

### Creating basic tables

In order for timetable to work you have to create timetable. This is several tables in SQLite, which should
be created before start (or you will get an error).

First, activate Django shell (it's necessary to load Django settings). You need to run this command in the
folder, where `manage.py` is located.

```bash
python manage.py shell
```

Then type in this:

```python
from main.db_connection import create_time_tables

create_time_tables()
```

When completed you should see message "Basic time tables created." in your console.

### Setting up settings

You need to open file called .env-example.

Insert Django `SECRET_KEY` - you can generate it using command:

```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Choose, whether the program should be in `DEBUG` mode or not (`True` or `False`).
If you're running program on specific website, specify it's url in `ALLOWED_HOST`.

The program uses SMTP protocol to send emails.
You should prepare email in order to do this and acquire necessary settings.
[Google email service](https://support.google.com/a/answer/176600?hl=en) is recommended.

**IMPORTANT:**
Then save the file as `.env` (change the file extension).

### Running program

Execute entry point, called "runserver" (for Windows - you need to run it through bash console):

```bash
./runserver
```

## Configuration

In the `config.yaml` you can see configs for this project.

Parameter `daily_update_hour` contains the time of daily updating of tables (in hours). Update is a
`Celery` task, which updates dates and available time in basic timetables.

Parameters in `lesson_settings` contain the minimum and maximum lesson time. User cannot enroll in
lesson, if his time exceeds the maximum or less than the minimum.

Parameters in `teacher_info` will be shown on the `Contacts` page.

Parameters in `default_available_time` contain default time for every day. This time will be shown, if
no one has enrolled in lesson. And daily update will reset time in timetable to this default settings.
When you change this parameters, you need to do this in order to apply changes to database:

1. Activate Django shell.
```bash
python manage.py shell
```

2. Run this Python function.
```python
from main.business_logic.available_time_controller import set_default_time

set_default_time()
```

## Technologies

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io/)
- [SQLite](https://www.sqlite.org/index.html)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [pytest](https://github.com/pytest-dev/pytest/)

## File structure

Coming soon...

## Testing

Make sure you have installed `pytest` package (it is also stated in `requirements.txt`).

To run all the tests use:

```bash
pytest -v
```