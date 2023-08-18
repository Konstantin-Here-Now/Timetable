# Timetable

...

## Contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Technologies](#technologies)
- [File structure](#file-structure)
- [Testing](#testing)

## Requirements

To use the project, you need to install [Python 3.10](https://www.python.org/downloads/release/python-3100/).

Other requirements should be installed via (check [Quick start](#quick-start)):

```bash
pip install -r requirements.txt
```

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

Install necessary libraries for Python:

```bash
pip install -r requirements.txt
```

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

Run entry point, called "runserver" (for Windows - you need to run it through bash console):

```bash
./runserver
```

## Configuration

Coming soon...

## Technologies

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io/)
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