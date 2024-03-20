FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY ./tracker_api /api/tracker_api

CMD ["uvicorn", "tracker_api.main:app", "--host", "0.0.0.0", "--port", "80"]