from typing import Optional, Union
from requests import get, post, Response, RequestException


URL_USERS = 'http://localhost/users'
URL_USER_DETAIL = 'http://localhost/users/{user_id}'
URL_USER_CIGARETTE = 'http://localhost/users/{user_id}/cigarettes'

BAD_REQUEST = 'Ошибка запроса к API {error}. Эндпоинт: {url}'
NOT_OK_STATUS = ('Запрос к API вернул код ответа "{status}". Эндпоинт: {url}')


class NotOkStatusResponseError(Exception):
    """Код ответа отличен от 200."""


class BotAPI:

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
        return self.post_api_answer(URL_USERS, {'telegram_id': telegram_id})

    def get_user_id(self, telegram_id: int) -> int:
        """Найти id пользователя в базе по telegram_id."""
        return self.get_api_answer(
            URL_USERS, {'telegram_id': telegram_id}
        )[0]['id']

    def get_or_create_user_id(self, telegram_id: int) -> int:
        """
        Найти или добавить пользователя по telegram_id и получить его id.
        """
        id = self.get_user_id(telegram_id)
        if not id:
            id = self.add_user(telegram_id).json()[0]['id']
        return id

    def add_user_cigarette(self, telegram_id: int,
                           smoking_time: str) -> Response:
        """Добавить запись о выкуренной сигарете."""
        id = self.get_or_create_user_id(telegram_id)
        return self.post_api_answer(
            url=URL_USER_CIGARETTE.format(user_id=id),
            params={'smoking_time': smoking_time}
        )

    def get_last_cigarettes(self, telegram_id: int) -> list:
        """Получить записи о последних сигаретах."""
        id = self.get_or_create_user_id(telegram_id)
        return self.get_api_answer(url=URL_USER_CIGARETTE.format(user_id=id))
