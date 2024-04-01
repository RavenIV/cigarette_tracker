from typing import Optional, Union
from requests import get, post, Response, RequestException


URL_USERS = 'http://{host}/users'
URL_USER_DETAIL = 'http://{host}/users/{user_id}'
URL_USER_CIGARETTE = 'http://{host}/users/{user_id}/cigarettes'

BAD_REQUEST = 'Ошибка запроса к API {error}. Эндпоинт: {url}'
NOT_OK_STATUS = ('Запрос к API вернул код ответа "{status}". Эндпоинт: {url}')


class NotOkStatusResponseError(Exception):
    """Код ответа отличен от 200."""


class BotAPI:

    def __init__(self, host: str):
        self.host = host

    @staticmethod
    def check_status(response: Response, url: str):
        if response.status_code != 200:
            raise NotOkStatusResponseError(NOT_OK_STATUS.format(
                status=response.status_code, url=url
            ))
        return response

    def get_api_answer(self, url: str, params: Optional[dict] = None):
        """Отправить GET запрос к API и вернуть json."""
        try:
            response = get(url=url, params=params)
        except RequestException as error:
            raise ConnectionError(BAD_REQUEST.format(error=error, url=url))
        return self.check_status(response, url=url).json()

    def post_api_answer(self, url: str,
                        params: dict[str, Union[int, str]]) -> Response:
        """Отправить POST запрос к API."""
        try:
            response = post(url=url, json=params)
        except RequestException as error:
            raise ConnectionError(
                BAD_REQUEST.format(error=error, url=url)
            )
        return self.check_status(response, url=url)

    def add_user(self, telegram_id: int) -> Response:
        """Добавить пользователя в базу."""
        url = URL_USERS.format(host=self.host)
        return self.post_api_answer(url, {'telegram_id': telegram_id})

    def get_or_create_user_id(self, telegram_id: int) -> int:
        """Найти или добавить пользователя по telegram_id и получить его id."""
        data = self.get_api_answer(
            URL_USERS.format(host=self.host),
            {'telegram_id': telegram_id}
        )
        if data:
            return data[0]['id']
        id = self.add_user(telegram_id).json()[0]['id']
        return id

    def add_user_cigarette(self, telegram_id: int,
                           smoking_time: str) -> Response:
        """Добавить запись о выкуренной сигарете."""
        id = self.get_or_create_user_id(telegram_id)
        return self.post_api_answer(
            URL_USER_CIGARETTE.format(host=self.host, user_id=id),
            {'smoking_time': smoking_time}
        )

    def get_last_cigarettes(self, telegram_id: int) -> list:
        """Получить записи о последних сигаретах."""
        id = self.get_or_create_user_id(telegram_id)
        return self.get_api_answer(
            URL_USER_CIGARETTE.format(host=self.host, user_id=id)
        )
