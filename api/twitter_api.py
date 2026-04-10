from utils.config import *


def post_tweet(alert_code):
    if alert_code == WARNING_CODE[0]:
        message = WARNING_MESSAGE
    elif alert_code == DANGER_CODE[0]:
        message = DANGER_MESSAGE
    elif alert_code == EMERGENCY_CODE[0]:
        message = EMERGENCY_MESSAGE
    elif alert_code <= SAFE_CODE[0]:
        message = SAFE_MESSAGE
    else:
        message = UNKNOWN_MESSAGE

    try:
        response = client.create_tweet(text=message)
        if response.status_code != 201:
            logger.error('Twitter API returned an error: %s', response.json())
        elif response.status_code == 201:
            logger.info('Twitter API returned successfully: %s', response.json())
        else:
            logger.warning('Twitter API returned an error: %s', response.json())
    except requests.exceptions.RequestException as e:
        logger.error('Twitter API is unreachable: %s', e)


