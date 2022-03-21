'''
Created on Mar 14, 2022

@author: rusty
'''

import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json


class Mqtt_zigbee(object):
    '''
    classdocs
    '''

    def __init__(self, sensors):
        '''
        Constructor
        '''

        self.sensors = sensors

        self.client = mqtt.Client()

        self.client.on_message = self.on_message

        self.client.connect("192.168.50.5")

        self.client.subscribe("zigbee2mqtt/temperature/+")

        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        # print("{} {}".format(msg.topic, msg.payload.decode()))

        if "temperature" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 3:
                return

            sensor_name = sensor[2].replace("_", " ")

            # convert celsius to fahrenheit
            tempt = round(1.8000 * float(json.loads(msg.payload.decode())["temperature"]) + 32, 1)

            now = datetime.now()

            if sensor_name in self.sensors.keys():
                frame = self.sensors[sensor_name][2]
                self.sensors[sensor_name] = [now.strftime("%H:%M"), tempt, frame]
            else:
                self.sensors[sensor_name] = [now.strftime("%H:%M"), tempt, None]


if __name__ == '__main__':
    sensors = dict()

    mqtt = Mqtt_zigbee(sensors)

    while True:
        time.sleep(1)
        # print("sensors: {}".format(sensors))
        print("---")
        for sensor, tempt in sensors.items():
            print("{}: {}: {} ({})".format(tempt[0], sensor, tempt[1], tempt[2]))

    print("done")
