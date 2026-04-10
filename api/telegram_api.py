from utils.config import *


def post_telegram(alert_code):
    if alert_code == WARNING_CODE[0]:
        send_to_telegram(WARNING_MESSAGE)
    elif alert_code == DANGER_CODE[0]:
        send_to_telegram(DANGER_MESSAGE)
    elif alert_code == EMERGENCY_CODE[0]:
        send_to_telegram(EMERGENCY_MESSAGE)
    elif alert_code <= SAFE_CODE[0]:
        send_to_telegram(SAFE_MESSAGE)
    else:
        send_to_telegram(UNKNOWN_MESSAGE)


def send_to_telegram(message):
    try:
        response = requests.post(api_url, json={'chat_id': chat_id, 'text': message})
        if response.status_code != 200:
            logger.error('Telegram API returned an error: %s', response.json())
        elif response.status_code == 200:
            logger.info('Telegram API returned successfully: %s', response.json())
        else:
            logger.warning('Telegram API returned an error: %s', response.json())
    except requests.exceptions.RequestException as e:
        logger.error('Telegram API is unreachable: %s', e)
