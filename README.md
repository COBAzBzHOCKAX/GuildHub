# GuildHub Project README
## Language Versions / Версии языка
- [English](README.md)
- [Русский](README_ru.md)

### Project Name: Guild Hub
[link to the project](https://github.com/COBAzBzHOCKAX/GuildHub "link to the project")

### Project Overview
**GuildHub** is a web application developed for a fan server of a well-known MMORPG. It provides a platform for users to post and manage announcements, exchange messages, and receive notifications. The project was developed from scratch by a single developer as a final project.

### Requirements
To install and run the project, you'll need the following components:
- Python 3.x
- Django 3.x
- Packages listed in `requirements.txt`
- Redis (for Celery)
- GIT (if using Windows)

### Installation
#### Чтобы установить проект локально, выполните следующие шаги:
1. ##### Clone the repository:
```bash
git clone https://github.com/COBAzBzHOCKAX/GuildHub.git
cd GuildHub
```

2. ##### Set up virtual environment (optional):
```shell
# cmd
python -m venv venv
venv\Scripts\activate
```
```bash
# bash
python -m venv .venv
source venv/bin/activate
```

3. ##### Install dependencies:
```bash
pip install -r requirements.txt
```

4. ##### Configure environment variables:
Create a .env file in the root directory of the GuildHub project with the following variables:
```
SECRET_KEY_DJANGO=your_django_secret_key
HOST_EMAIL_MAIL_RU=your_email@mail.ru
HOST_EMAIL_MAIL_RU_PASSWORD=your_email_password
ADMINS=admin1@example.com,admin2@example.com
```

5. ##### Project Settings:
Adjust project settings in GuildHub/config/settings.py to match your local setup:
 - Set appropriate values for `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CELERY_ACCEPT_CONTENT`, `CELERY_TASK_SERIALIZER`, `CELERY_RESULT_SERIALIZER`
 - For deployment, ensure `DEBUG = False`, specify `ALLOWED_HOSTS`, and set `SITE_URL`.

### Running the Project
To run the project, run the following commands:
#### Navigate to the Django project root:
```bash
cd GuildHub
```

#### Apply database migrations:
```bash
python manage.py migrate
```

#### Create the first superuser
```bash
python manage.py createsuperuser  # follow the instructions
```

#### Run the Django server:
```bash
python manage.py runserver
```

#### Start Celery for asynchronous tasks:
```bash
celery -A config worker -l INFO
```
**This command may not work on Windows!**\
Use the following command:
```shell
celery -A config worker -l INFO --pool solo
```

### Configuration
Additional project configurations can be adjusted by modifying configuration files according to your development or production environment needs.

### Usage
After setting up, use the web interface to create, view, and manage announcements, exchange messages, and utilize other application features.

### Contribution and Development
This project was created solely for educational purposes, and further development is not planned.

### License
This project is licensed under the terms of the MIT License.

### Authors
Project Author: COBA_B_HOCKAX (Danila)\
GitHub: https://github.com/COBAzBzHOCKAX \
Telegram: https://t.me/COBA_B_HOCKAX
