FROM python:3.10

WORKDIR /bot

COPY ./requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

COPY . .

CMD ["python", "bot.py"]