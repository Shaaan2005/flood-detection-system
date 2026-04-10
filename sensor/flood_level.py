import asyncio
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from api.telegram_api import post_telegram
# from api.twitter_api import post_tweet
from databases import Database
from utils.config import get_timestamp, database

# Raspberry Pi pin configuration:
RST = 24

HSCR04_OUT = 20
HSCR04_IN = 21

LEDr = 13
LEDy = 19
LEDg = 26

BUZZ = 25

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(HSCR04_OUT, GPIO.OUT)
GPIO.setup(HSCR04_IN, GPIO.IN)

GPIO.setup(LEDg, GPIO.OUT)
GPIO.setup(LEDy, GPIO.OUT)
GPIO.setup(LEDr, GPIO.OUT)
GPIO.setup(BUZZ, GPIO.OUT)





print('uitvoeren...')

disp.begin()
# Clear display.
disp.clear()
disp.display()
measurements_list = []

def alert_bot(alert_code):
    # post_tweet(alert_code)
    post_telegram(alert_code)

measurements_list = []

def alert_bot(alert_code):
    # post_tweet(alert_code)
    post_telegram(alert_code)

async def insert_sensor_data(alert_code, alert_name, water_level, time_stamp):
    

    query_get = "SELECT * FROM Alerts"
    results_get = await database.fetch_all(query=query_get)

    if results_get[-1][1] != alert_code:
        values_1 = [(alert_code, alert_name, time_stamp)]
        query_1 = 'INSERT INTO Alerts (alert_code, alert_name, timestamp) VALUES{}'.format(', '.join(map(str, values_1)))
        results_1 = await database.execute(query=query_1)

        values_2 = [(water_level, time_stamp)]
        query_2 = 'INSERT INTO WaterLevel (level, timestamp) VALUES{}'.format(', '.join(map(str, values_2)))
        results_2 = await database.execute(query=query_2)

        alert_bot(alert_code)

def siren():
    x = 0
    while x < 10:
        GPIO.output(BUZZ, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(BUZZ, GPIO.LOW)
        time.sleep(0.25)
        x += 1



def get_distance():
    GPIO.output(HSCR04_OUT, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(HSCR04_OUT, GPIO.LOW)

    while GPIO.input(HSCR04_IN) == GPIO.LOW:
        start_time = time.time()
    while GPIO.input(HSCR04_IN) == GPIO.HIGH:
        end_time = time.time()
    sig_time = end_time - start_time

    distance = sig_time / 0.000058
    return distance

def update_alarm_code(distance):
    print(distance)
    GPIO.output(LEDg, GPIO.LOW)
    GPIO.output(LEDy, GPIO.LOW)
    GPIO.output(LEDr, GPIO.LOW)
    GPIO.output(BUZZ, GPIO.LOW)

    if 6 < distance <= 9:
        alert_code = 1
    elif 4 < distance <= 6:
        alert_code = 2
    elif distance <= 4:
        GPIO.output(LEDr, GPIO.HIGH)
        alert_code = 3
    else:
        alert_code = 0
        alert_name = "SAFE"
        GPIO.output(LEDg, GPIO.HIGH)
    if alert_code == 1:
        alert_image = 'nood1.png'
        alert_name = "WARNING"
        GPIO.output(LEDy, GPIO.HIGH)
    elif alert_code == 2:
        alert_image = 'nood2.png'
        alert_name = "DANGER"
        GPIO.output(LEDr, GPIO.HIGH)
    elif alert_code == 3:
        alert_image = 'nood3.png'
        alert_name = "EMERGENCY"
        GPIO.output(LEDr, GPIO.HIGH)
        GPIO.output(BUZZ, GPIO.HIGH)
        
    else:
        alert_image = 'nood0.png'
    image = Image.open("../SmartCity-Flood-Detection/sensor/" + alert_image).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    
    disp.clear()
    # Display image.
    disp.image(image)
    disp.display()
    if alert_code == 3:
        siren()
    disp.clear()

    asyncio.run(insert_sensor_data(alert_code, alert_name, distance, get_timestamp()[2]))


def average(lst):
    return round(sum(lst) / len(lst))

def clamp(n, smallest, largest): return max(smallest, min(n, largest))


distance_list = []
def start_measuring():
    distance = round(get_distance())
    distance = clamp(distance, 1, 20)
    distance_list.append(distance)
    time.sleep(3)
    if len(distance_list) > 5:
        distance_list.pop(0)
        update_alarm_code(average(distance_list))
    else:
        print(distance)

