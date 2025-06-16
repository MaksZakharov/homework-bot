import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
from telebot import TeleBot

from constants import (
    RETRY_PERIOD, ENDPOINT, HOMEWORK_VERDICTS,
    MISSING_REQUIRED_TOKENS, NO_NEW_STATUSES, MESSAGE_SEND,
    ERROR_SEND_MESSAGE, ERROR_REQUEST_API, ENDPOINT_ERROR,
    API_TYPE_ERROR, MISSING_HOMEWORKS_KEY, HOMEWORKS_NOT_LIST,
    MISSING_HOMEWORK_NAME_KEY, MISSING_STATUS_KEY, UNKNOWN_STATUS
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def check_tokens():
    """Проверяет наличие обязательных переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправляет сообщение в Telegram-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(MESSAGE_SEND.format(message=message))
    except Exception as error:
        logging.error(ERROR_SEND_MESSAGE.format(error=error))


def get_api_answer(timestamp):
    """Делает запрос к API Практикум.Домашка."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
        if response.status_code != 200:
            raise Exception(ENDPOINT_ERROR.format(
                endpoint=ENDPOINT, status_code=response.status_code
            ))
        return response.json()
    except Exception as error:
        raise Exception(ERROR_REQUEST_API.format(error=error))


def check_response(response):
    """Проверяет корректность структуры ответа API."""
    if not isinstance(response, dict):
        raise TypeError(API_TYPE_ERROR)

    if 'homeworks' not in response:
        raise KeyError(MISSING_HOMEWORKS_KEY)

    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError(HOMEWORKS_NOT_LIST)

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
    if not check_tokens():
        logging.critical(MISSING_REQUIRED_TOKENS)
        sys.exit(1)

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
                send_message(bot, message)
            else:
                logging.debug(NO_NEW_STATUSES)

            timestamp = response.get('current_date', timestamp)
            time.sleep(RETRY_PERIOD)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if message != last_error:
                send_message(bot, message)
                last_error = message
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
