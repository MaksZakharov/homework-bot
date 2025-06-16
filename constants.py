# constants.py

# Настройки API и задержка
RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'

# Возможные статусы домашней работы
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

# Сообщения и ошибки
MISSING_REQUIRED_TOKENS = (
    'Отсутствует обязательная переменная окружения. Работа бота остановлена.'
)
NO_NEW_STATUSES = 'Нет новых статусов.'
MESSAGE_SEND = 'Отправлено сообщение: {message}'
MESSAGE_SEND_IN_TG = 'Сообщение отправлено в Telegram: {message}'
ERROR_SEND_MESSAGE = 'Ошибка при отправке сообщения: {error}'
ERROR_REQUEST_API = 'Ошибка при запросе к API: {error}'
ENDPOINT_ERROR = (
    'Эндпоинт {endpoint} недоступен. Код ответа API: {status_code}'
)
API_TYPE_ERROR = 'Ответ API должен быть словарем.'
MISSING_HOMEWORKS_KEY = 'В ответе отсутствует ключ "homeworks".'
HOMEWORKS_NOT_LIST = 'Значение "homeworks" должно быть списком.'
MISSING_HOMEWORK_NAME_KEY = 'В ответе API нет ключа "homework_name".'
MISSING_STATUS_KEY = 'В ответе API нет ключа "status".'
UNKNOWN_STATUS = 'Неизвестный статус домашней работы: {status}'
ERROR_PROGRAM_FAILURE = 'Сбой в работе программы: {error}'
REPEATED_ERROR = 'Повторная ошибка: {error}. Сообщение уже отправлялось ранее.'
TOKENS_ARE_VALID = 'Все обязательные переменные окружения заданы.'
START_CHECKING = 'Начинаю проверку новых домашних работ.'
FINISHED_CHECKING = 'Проверка домашних работ завершена.'
EMPTY_API_RESPONSE = 'API вернул пустой ответ.'
EMPTY_HOMEWORKS = 'В ответе API нет новых домашних работ.'
JSON_DECODE_ERROR = (
    'Ошибка декодирования JSON при парсинге ответа API: {error}'
)
ERROR_MESSAGE_TIMESTAMP_NOT_UPDATED = (
    'Не удалось обновить timestamp — время последней проверки не обновлено.'
)
