import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import logging

#===============================================================================
# values from 433mhz sensors are fed to mqtt via the rtl_433 linux program
# with rtl_433 -C customary -F "mqtt://localhost:1883,events=rtl_433[/model]"
#===============================================================================


class Mqtt_rtl433(object):

    def __init__(self, sensor_values):
        self.sensor_names = {"Prologue-TH":"outside",
                             "Acurite-Tower":"garage",
                             "Oregon-THGR122N":"attic"}

        self.sensor_values = sensor_values

        self.logger = logging.getLogger('sensors.rtl433')

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

        if "temperature_F" in json.loads(msg.payload.decode()):
            sensor = msg.topic.split("/")
            if len(sensor) != 2:
                return

            if sensor[1] not in self.sensor_names.keys():
                return

            sensor_name = self.sensor_names[sensor[1]]

            tempt = round(float(json.loads(msg.payload.decode())["temperature_F"]), 1)

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
            self.client.subscribe("rtl_433/#", qos = 2)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.warn("unexpected disconnection")


# debug main
if __name__ == '__main__':
    sensors = dict()

    mqtt = Mqtt_rtl433(sensors)

    while True:
        time.sleep(1)
        # print("sensor_values: {}".format(sensor_values))
        print("---")
        for sensor in sensors.keys():
            print("{}".format(sensor))

    print("done")
