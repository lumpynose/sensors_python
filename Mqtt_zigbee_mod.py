import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import logging


class Mqtt_zigbee(object):

    def __init__(self, sensor_values):
        self.sensor_values = sensor_values

        self.logger = logging.getLogger('sensor.zigbee')

        self.client = mqtt.Client()

        self.client.reconnect_delay_set(min_delay = 1, max_delay = 120)

        self.client.enable_logger(self.logger)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.client.connect("192.168.50.5")

        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        self.logger.debug("{} {}".format(msg.topic, msg.payload.decode()))

        if "temperature" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 3:
                return

            sensor_name = sensor[2].replace("_", " ")

            # convert celsius to fahrenheit
            tempt = round(1.8000 * float(json.loads(msg.payload.decode())["temperature"]) + 32, 1)

            now = datetime.now()

            if sensor_name in self.sensor_values.keys():
                self.sensor_values[sensor_name]["time"] = now.strftime("%H:%M")
                self.sensor_values[sensor_name]["temperature"] = tempt
            else:
                self.sensor_values.update({sensor_name:
                                  {"time": now.strftime("%H:%M"),
                                   "temperature": tempt}})

    def on_connect(self, client, userdata, flags, rc):
        self.logger.debug("connected: {}".format(rc))

        if rc == 0:
            self.client.subscribe("zigbee2mqtt/temperature/#", qos = 2)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.debug("unexpected disconnection")


# debug main
if __name__ == '__main__':
    sensors = dict()

    mqtt = Mqtt_zigbee(sensors)

    while True:
        time.sleep(1)
        # print("sensor_values: {}".format(sensor_values))
        print("---")
        for sensor, tempt in sensors.items():
            print("{}".format(sensor))

    print("done")
