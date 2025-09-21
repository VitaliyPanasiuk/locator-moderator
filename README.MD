Цей темплейт використовується для розробки Telegram ботів з використанням бібліотеки [`aiogram v3.0+`]

### Для того, щоб почати використовувати:
1. Скопіюйте `.env.dist` в `.env` i заповніть необхідні дані.
BOT_TOKEN=BOT_TOKEN
USE_REDIS=False
DB_HOST=localhost
DB_PASS=your_password
DB_USER=your_user
DB_NAME=your_db

2. bot_project/bot_project/settings.py set DB data in dic DATABASES 

3. **Встановлення віртуального середовища та модулів**
   1. Створіть [venv] `python -m venv venv`
   2. Встановить залежності із requirements.txt: `pip install -r requirements.txt`
   3. Запустіть проєкт з команди `python3 bot.py`
4. **Запуск админки**
   `cd bot_project`
   `python manage.py createsuperuser` -> для создания аакунта на вход в админку
   `python manage.py runserver`

   к ссылке добавить /admin что бы попасть в админку