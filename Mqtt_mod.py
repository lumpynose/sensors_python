import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import logging


class Mqtt(object):

    def __init__(self, sensor_values):
        self.rtl433_sensor_names = {"Prologue-TH":"outside",
                             "Acurite-Tower":"garage",
                             "Oregon-THGR122N":"attic"}

        self.sensor_values = sensor_values

        self.logger = logging.getLogger('sensors.rtl433')

        self.client = mqtt.Client()

        self.client.reconnect_delay_set(min_delay = 1, max_delay = 120)

        self.client.enable_logger(self.logger)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

        self.client.message_callback_add("rtl_433/#",
                    self.on_message_rtl433)

        self.client.message_callback_add("zigbee2mqtt/temperature/#",
                    self.on_message_zigbee)

        self.client.connect("192.168.50.5")

        self.client.loop_start()

    def on_message_rtl433(self, client, userdata, msg):
        self.logger.debug("{} {}".format(msg.topic, msg.payload.decode()))

        if "temperature_F" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 2:
                return

            if sensor[1] not in self.rtl433_sensor_names.keys():
                return

            sensor_name = self.rtl433_sensor_names[sensor[1]]

            tempt = round(float(json.loads(msg.payload.decode())["temperature_F"]), 1)

            now = datetime.now()

            if sensor_name in self.sensor_values.keys():
                self.sensor_values[sensor_name]["time"] = now.strftime("%H:%M")
                self.sensor_values[sensor_name]["temperature"] = tempt
            else:
                self.sensor_values.update({sensor_name:
                                  {"time": now.strftime("%H:%M"),
                                   "temperature": tempt}})

    def on_message_zigbee(self, client, userdata, msg):
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
            self.client.subscribe([("zigbee2mqtt/temperature/#", 2),
                        ("rtl_433/#", 2)])

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.warn("unexpected disconnection")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.debug("granted_qos: {}".format(granted_qos))
