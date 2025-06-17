# Настройки API и задержка
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
RETRY_PERIOD = 600

# Возможные статусы домашней работы
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'rejected': 'Работа проверена: у ревьюера есть замечания.',
    'reviewing': 'Работа взята на проверку ревьюером.'
}

# Сообщения и ошибки
API_TYPE_ERROR = (
    'Ответ API должен быть словарем, но получен тип: {actual_type}.'
)
ATTEMPT_SEND_MESSAGE = 'Попытка отправить сообщение: {message}'
EMPTY_API_RESPONSE = 'API вернул пустой ответ.'
EMPTY_HOMEWORKS = 'В ответе API нет новых домашних работ.'
ENDPOINT_ERROR = (
    'Эндпоинт {endpoint} недоступен. Код ответа API: {status_code}'
)
ERROR_MESSAGE_TIMESTAMP_NOT_UPDATED = (
    'Не удалось обновить timestamp — время последней проверки не обновлено.'
)
ERROR_PROGRAM_FAILURE = 'Сбой в работе программы: {error}'
ERROR_REQUEST_API = 'Ошибка при запросе к API: {error}'
ERROR_SEND_MESSAGE = 'Ошибка при отправке сообщения: {error}'
FINISHED_CHECKING = 'Проверка домашних работ завершена.'
HOMEWORKS_NOT_LIST = (
    'Значение "homeworks" должно быть списком, но получен тип: {actual_type}.'
)
JSON_DECODE_ERROR = (
    'Ошибка декодирования JSON при парсинге ответа API: {error}'
)
MESSAGE_SEND = 'Отправлено сообщение: {message}'
MESSAGE_SEND_IN_TG = 'Сообщение отправлено в Telegram: {message}'
MISSING_ENV_VARS = 'Отсутствуют обязательные переменные окружения: {vars}'
MISSING_HOMEWORKS_KEY = 'В ответе отсутствует ключ "homeworks".'
MISSING_HOMEWORK_NAME_KEY = 'В ответе API нет ключа "homework_name".'
MISSING_STATUS_KEY = 'В ответе API нет ключа "status".'
NO_NEW_STATUSES = 'Нет новых статусов.'
REPEATED_ERROR = 'Повторная ошибка: {error}. Сообщение уже отправлялось ранее.'
START_CHECKING = 'Начинаю проверку новых домашних работ.'
TOKENS_ARE_VALID = 'Все обязательные переменные окружения заданы.'
UNKNOWN_STATUS = 'Неизвестный статус домашней работы: {status}'
