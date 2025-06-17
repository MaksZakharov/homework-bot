class APIRequestError(Exception):
    """Ошибка при запросе к API (проблема с сетью или с requests)."""

    pass


class APIResponseError(Exception):
    """Ошибка в ответе API (неожиданный статус-код, неверный статус-код)."""

    pass


class MissingTokensError(Exception):
    """Отсутствуют обязательные переменные окружения."""

    pass
