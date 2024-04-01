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

Создать образ и запустить контейнер API сервиса из директории api/:

```
сd api/
```
```
docker build -t myimage .
```
```
docker run -d --name mycontainer -p 80:80 myimage
```

Перейти в директорию bot/, создать и активировать виртуальное окружение, установить зависимости:

```
cd ../bot/
```
```
python -m venv venv
```

- Для пользователей mac/Linux

  ```
  source venv/bin/activate/
  ```
  
- Для пользователей Windows

  ```
  source env/scripts/activate
  ```

```
pip install -r requirements.txt
```

Создать файл .env в директории bot/ и указать токен бота в переменной TELEGRAM_TOKEN

Запустить бота:

```
python bot.py
```

## Авторы:

- концепция, ревью: Николай Иванцов [GitHub](https://github.com/mikolainer) 
- разработка: Ирина Воронцова [GitHub](https://github.com/RavenIV)
