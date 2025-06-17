import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from telebot import TeleBot
from telebot.apihelper import ApiException

from constants import (
    API_TYPE_ERROR, ATTEMPT_SEND_MESSAGE, ENDPOINT, ENDPOINT_ERROR,
    ERROR_REQUEST_API, ERROR_SEND_MESSAGE, HOMEWORKS_NOT_LIST,
    HOMEWORK_VERDICTS, MESSAGE_SEND, MISSING_ENV_VARS,
    MISSING_HOMEWORK_NAME_KEY, MISSING_HOMEWORKS_KEY, MISSING_STATUS_KEY,
    NO_NEW_STATUSES, RETRY_PERIOD, UNKNOWN_STATUS
)
from exceptions import APIRequestError, APIResponseError, MissingTokensError

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


def check_tokens():
    """Проверяет наличие обязательных переменных окружения.
    и сообщает о недостающих.
    """
    tokens = [
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    ]
    missing_tokens = [name for name, value in tokens if not value]

    if missing_tokens:
        message = MISSING_ENV_VARS.format(
            vars=', '.join(missing_tokens)
        )
        logging.critical(message)
        raise MissingTokensError(message)


def send_message(bot, message):
    """Отправляет сообщение в Telegram-чат. Возвращает True/False."""
    try:
        logging.debug(ATTEMPT_SEND_MESSAGE.format(message=message))
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(MESSAGE_SEND.format(message=message))
        return True
    except (ApiException, RequestException) as error:
        logging.error(ERROR_SEND_MESSAGE.format(error=error))
        return False


def get_api_answer(timestamp):
    """Делает запрос к API Практикум.Домашка."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException as error:
        raise APIRequestError(ERROR_REQUEST_API.format(error=error))

    if response.status_code != HTTPStatus.OK:
        raise APIResponseError(ENDPOINT_ERROR.format(
            endpoint=ENDPOINT, status_code=response.status_code
        ))

    return response.json()


def check_response(response):
    """Проверяет корректность структуры ответа API."""
    if not isinstance(response, dict):
        raise TypeError(API_TYPE_ERROR.format(
            actual_type=type(response).__name__)
        )

    if 'homeworks' not in response:
        raise KeyError(MISSING_HOMEWORKS_KEY)

    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError(HOMEWORKS_NOT_LIST.format(
            actual_type=type(homeworks).__name__)
        )
    return homeworks


def parse_status(homework):
    """Извлекает статус домашней работы из словаря homework."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError(MISSING_HOMEWORK_NAME_KEY)

    status = homework.get('status')
    if status is None:
        raise KeyError(MISSING_STATUS_KEY)

    verdict = HOMEWORK_VERDICTS.get(status)
    if verdict is None:
        raise ValueError(UNKNOWN_STATUS.format(status=status))

    return (f'Изменился статус проверки работы "{homework_name}". '
            f'{verdict}')


def main():
    """Основная логика работы бота."""
    check_tokens()

    bot = TeleBot(TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_error = None

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)

            if homeworks:
                homework = homeworks[0]
                message = parse_status(homework)
                if send_message(bot, message):
                    timestamp = response.get('current_date', timestamp)
                    last_error = None
            else:
                logging.debug(NO_NEW_STATUSES)
                timestamp = response.get('current_date', timestamp)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if message != last_error:
                if send_message(bot, message):
                    last_error = message

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    main()
