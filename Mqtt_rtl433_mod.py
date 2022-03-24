import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import logging


class Mqtt_rtl433(object):

    def __init__(self, sensor_values):
        self.sensor_names = ("Prologue-TH", "Acurite-Tower", "Oregon-THGR122N")

        self.sensor_values = sensor_values

        self.logger = logging.getLogger('sensors.rtl433')

        self.client = mqtt.Client()

        self.client.on_message = self.on_message

        self.client.connect("192.168.50.5")

        self.client.subscribe("rtl_433/#")

        self.client.reconnect_delay_set(min_delay = 1, max_delay = 120)

        self.client.enable_logger(self.logger)

        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        self.logger.debug("{} {}".format(msg.topic, msg.payload.decode()))

        if "temperature_F" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 2:
                return

            sensor_name = sensor[1]

            if sensor_name not in self.sensor_names:
                return

            tempt = float(json.loads(msg.payload.decode())["temperature_F"])

            now = datetime.now()

            if sensor_name in self.sensor_values.keys():
                self.sensor_values[sensor_name]["time"] = now.strftime("%H:%M")
                self.sensor_values[sensor_name]["temperature"] = tempt
            else:
                self.sensor_values.update({sensor_name:
                                  {"time": now.strftime("%H:%M"),
                                   "temperature": tempt}})


if __name__ == '__main__':
    sensors = dict()

    mqtt = Mqtt_rtl433(sensors)

    while True:
        time.sleep(1)
        # print("sensor_values: {}".format(sensor_values))
        print("---")
        for sensor, tempt in sensors.items():
            print("{}: {}: {} ({})".format(tempt[0], sensor, tempt[1], tempt[2]))

    print("done")
