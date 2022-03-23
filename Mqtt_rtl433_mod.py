import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import logging

class Mqtt_rtl433(object):
    def __init__(self, sensors):
        self.sensor_names = ("Prologue-TH", "Acurite-Tower", "Oregon-THGR122N")

        self.sensors = sensors

        self.client = mqtt.Client()

        self.client.on_message = self.on_message

        self.client.connect("192.168.50.5")

        self.client.subscribe("rtl_433/#")

        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        logging.debug("{} {}".format(msg.topic, msg.payload.decode()))

        if "temperature_F" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 2:
                return

            sensor_name = sensor[1]

            if sensor_name not in self.sensor_names:
                return

            tempt = float(json.loads(msg.payload.decode())["temperature_F"])

            now = datetime.now()

            if sensor_name in self.sensors.keys():
                frame = self.sensors[sensor_name][2]
                self.sensors[sensor_name] = [now.strftime("%H:%M"), tempt, frame]
            else:
                self.sensors[sensor_name] = [now.strftime("%H:%M"), tempt, None]


if __name__ == '__main__':
    sensors = dict()

    mqtt = Mqtt_rtl433(sensors)

    while True:
        time.sleep(1)
        # print("sensors: {}".format(sensors))
        print("---")
        for sensor, tempt in sensors.items():
            print("{}: {}: {} ({})".format(tempt[0], sensor, tempt[1], tempt[2]))

    print("done")
