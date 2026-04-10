from fastapi import FastAPI
from api.twitter_api import post_tweet
from api.telegram_api import post_telegram
from databases import Database
import threading
import time
from sensor.flood_level import start_measuring
import threading
import time
from sensor.flood_level import start_measuring
from utils.config import *



app = FastAPI()


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


def alert_bot(alert_code):
    post_tweet(alert_code)
    post_telegram(alert_code)


@app.post("/alert/send/{alert_code}")
def alert(alert_code: int):
    alert_bot(alert_code)
    return {"message": f"alerted with code: {alert_code}"}


@app.get("/water-level/all")
async def water_level():
    query = "SELECT * FROM WaterLevel"
    results = await database.fetch_all(query=query)
    return results


@app.get("/alerts/all")
async def alerts():
    # start_thread()
    query = "SELECT * FROM Alerts"
    results = await database.fetch_all(query=query)
    return results


@app.get("/alerts/trends")
async def alerts():
    query = "SELECT alert_name, count(*) FROM Alerts GROUP BY alert_name"
    results = await database.fetch_all(query=query)
    return results


@app.get("/water-level/trends")
async def alerts():
    query = "SELECT level, count(*) FROM WaterLevel GROUP BY level"
    results = await database.fetch_all(query=query)
    return results


@app.post("/manual-input")
async def insert_sensor_data(alert_code, alert_name, water_level):
    values_1 = [(alert_code, alert_name, get_timestamp()[2])]
    query_1 = 'INSERT INTO Alerts (alert_code, alert_name, timestamp) VALUES{}'.format(', '.join(map(str, values_1)))
    results_1 = await database.execute(query=query_1)

    values_2 = [(water_level, get_timestamp()[2])]
    query_2 = 'INSERT INTO WaterLevel (level, timestamp) VALUES{}'.format(', '.join(map(str, values_2)))
    results_2 = await database.execute(query=query_2)
    return results_1, results_2


def background_tasks():
    x = 0
    while x < 300:
        measurements = start_measuring()
        time.sleep(3)
        x+=1

@app.get("/sensor/start")
def start_thread():
    b = threading.Thread(target=background_tasks)
    b.start()
    print("Measuring started")
    return {"message": "Measuring started"}
    