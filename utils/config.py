from datetime import datetime
import requests
import tweepy
import logging

from databases import Database

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('utils/flood_api_logs.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Twitter API
consumer_key = "99Hpg1VQE6Q4ZxDC74y0qeRIa"
consumer_secret = "G1Yfbr1nDP1UBcE5oSwIEuHWzDf3IAhOV0SLY2Ld5z8Jy9SkKo"
access_token = "1598622610740465664-MdwNe0dQCrrVvblbgRHri6QTwFd1Hm"
access_token_secret = "kDRFjz8yk09DdgmdEYVplYqnhtWRJmEF3S8uYnhMjpnqo"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJLpjwEAAAAArtodUEnDtq1m75I4hYaoYbHACCI%3D9R8iaWrLCNONjWO7ov8qTlNmWoRIdueqXf9nUJI4V9hqwaZiHH"

try:
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret,
                           return_type=requests.Response,
                           wait_on_rate_limit=True)
except tweepy.errors.Unauthorized as e:
    logger.error('Twitter API is unreachable: %s', e)

# Telegram API
api_token = '5654463762:AAGsuzYgWh9qU6ZZm3md1Ag1wWGCWUpV-P0'
chat_id = '-1001817324728'
api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'

database = Database("sqlite:///utils/data.db")

def get_timestamp():
    now = datetime.now()
    current_datetime = now.isoformat()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")
    return current_time, current_date, current_datetime


SAFE_CODE = 0, "SAFE"
WARNING_CODE = 1, "WARNING"
DANGER_CODE = 2, "DANGER"
EMERGENCY_CODE = 3, "EMERGENCY"

WARNING_MESSAGE = "🟡 Warning! 🟡\n—————————\nThere is a flood in your area. Please be careful!\n\n"
DANGER_MESSAGE = "🟠 Danger! 🟠\n————————\nFlood is rising, prepare to evacuate!\n\n"
EMERGENCY_MESSAGE = "🔴 Emergency! 🔴\n——————————\nEvacuate immediately! Flood is rising rapidly!\n\n"
SAFE_MESSAGE = "🟢 All Good! 🟢\n—————————\nNo flood detected in your area. Stay safe!\n\n"

UNKNOWN_MESSAGE = "🟣 Flood level is unknown. 🟣\n————————————————\n Please check again later.\n\n"
