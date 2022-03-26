from tkinter import *
from tkinter import ttk

from Mqtt_zigbee_mod import Mqtt_zigbee
from Mqtt_rtl433_mod import Mqtt_rtl433
from Mqtt_mod import import Mqtt 

import logging
import os

global main_frame
global sensor_rows, sensor_values
global logger


def set_style():
    style = ttk.Style()

    style.configure("Main.TFrame", background = "Khaki",
        relief = "solid")
    style.configure("Sensor.TFrame", background = "DarkKhaki",
        relief = "solid")
    style.configure("Sensor.TLabel", background = "Olive",
        font = ("Arial Bold", 16))
    style.configure("Value.TLabel", background = "DarkSeaGreen",
        font = ("Arial Bold", 14))
    style.configure("ValueTime.TLabel", background = "DarkSeaGreen",
        font = ("Arial", 8))


def add_row(row, sensor):
    sensor_frame = ttk.Frame(main_frame, padding = (0, 8, 0, 8),
        style = "Sensor.TFrame")
    sensor_frame.grid(column = 0, row = row, sticky = (E, W))
    sensor_frame.columnconfigure(0, weight = 1, uniform = 1)

    l = ttk.Label(sensor_frame, text = sensor,
        anchor = "center", style = "Sensor.TLabel")
    l.grid(column = 0, row = 0, sticky = (E, W))

    temperature = StringVar(value = float(0.0))
    l = ttk.Label(sensor_frame, textvariable = temperature, anchor = "center",
        style = "Value.TLabel")
    l.grid(column = 0, row = 1, sticky = (E, W))

    time = StringVar(value = "00:00")
    l = ttk.Label(sensor_frame, textvariable = time, anchor = "center",
        style = "ValueTime.TLabel")
    l.grid(column = 0, row = 2, sticky = (E, W))

    sensor_rows.update({sensor:{"time":time, "temperature":temperature}})


def do_run():
    logger = logging.getLogger('sensors.do_run')

    # if len(sensor_values) == 0:
    logger.debug("sensors: {}".format(sensor_values))

    row = 0

    for sensor in sensor_values.keys():
        logger.debug("{}".format(sensor))

        if sensor not in sensor_rows.keys():
            logger.debug("add row: {}, {}".format(row, sensor))
            add_row(row, sensor)

        sensor_rows[sensor]["time"].set(sensor_values[sensor]["time"])
        sensor_rows[sensor]["temperature"].set(sensor_values[sensor]["temperature"])

        row = row + 1

    root.after(15 * 1000, do_run)


if __name__ == '__main__':
    log_file = "d:\\tmp\\temp.log"
    if os.path.exists(log_file):
        os.remove(log_file)
    logging.basicConfig(filename = log_file,
                        encoding = 'utf-8',
                        format = '%(asctime)s %(message)s',
                        datefmt = '%I:%M:%S',
                        level = logging.WARN)
    logger = logging.getLogger('sensors')

    root = Tk();

    root.title("temperatures")

    main_frame = ttk.Frame(root, style = "Main.TFrame")
    main_frame.grid(column = 0, row = 0, sticky = (N, S, E, W))
    main_frame.columnconfigure(0, weight = 1, uniform = 1)

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)

    sensor_rows = dict()
    sensor_values = dict()

    # mqz = Mqtt_zigbee(sensor_values)
    # mqr = Mqtt_rtl433(sensor_values)
    mqtt = Mqtt(sensor_values)

    set_style()

    root.after(1 * 1000, do_run)

    root.mainloop()
