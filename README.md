# Cigarette Tracker

В стадии разработки.

Телеграм-бот призван помочь курильщикам избавиться от вредной привычки через постепенное увеличение интервалов между сигаретами. 
На данном этапе бот показывает только московское время.

Для проекта также реализован API сервис для записи и чтения истории курения пользователей.

## Стек

- Python 3.10
- FastAPI 0.110.0
- SQLAlchemy 2.0.28
- Pydantic 2.6.4
- Uvicorn 0.28.1
- Docker
- Aiogram 3.4.1
- requests 2.31.0
- pytz 2024.1
- SQLite

## Запуск проекта

Установить [Docker](https://www.docker.com/).

Клонировать репозиторий и перейти в него в командной строке:

```
git clone <ssh link>
cd cigarette_tracker/
```

Создать файл .env в директории bot/ и указать токен бота в переменной TELEGRAM_TOKEN. 

Запустить контейнеры:

```
docker compose up
```

## Авторы:

- концепция, ревью - Николай Иванцов [GitHub](https://github.com/mikolainer) 
- разработка - Ирина Воронцова [GitHub](https://github.com/RavenIV)
