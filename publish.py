import paho.mqtt.client as mqtt

from beartype.typing import Dict, List, Tuple, Union, Annotated
from beartype import beartype
from beartype.roar import BeartypeCallHintParamViolation
from random import uniform
import time

# Define Variables
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "hiphop2025"
i = True
client = mqtt.Client("publisher")    #create client object
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start()

cities = {"karnataka": {"city": ["Bangalore", "Mysore"]},
          "Kerala": {"city":["Cochin"]}}

def get_cities(cities):
    """_summary_

    Args:
        cities (dict): All states and corresponding cities

    Returns:
        set: set of cities
    """
    all_cities = set(map(lambda x: x.get("city"), cities)) if cities else set()
    return all_cities


@beartype
def fetch_value(city: str, low_high: Union[Annotated[List[float], 2], str]) -> Dict[str, Union[str, int]]:
    """_summary_

    Args:
        city (str): city name
        low_high (Union[Annotated[List[float], 2], str]): low and high temperature values

    Returns:
        Dict[str, Union[str, int]]: temperate of city
    """
    if isinstance(low_high, str):
        response = {city: f"No temperature detected, obtained: {low_high}"}
    else:
        low, high = low_high
        response = {city: uniform(low, high)}
    return response

def publish(MQTT_TOPIC, client):
    try:
        current_value = fetch_value('Bangalore', [20.0, 21.0])
    except BeartypeCallHintParamViolation as e:
        print("Invalid Argument", str(e))
        global i
        i = False
        return "Invalid Argument"
    except Exception as e:
        print(str(e))
        return e
    client.publish(MQTT_TOPIC, current_value, qos=1)
    print("Just published " + str(current_value) + " to topic: ", MQTT_TOPIC)
    time.sleep(10)

while i == True:
    publish(MQTT_TOPIC, client)
    