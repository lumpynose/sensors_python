from tkinter import Tk, N, W, E, S
from tkinter import ttk

from Mqtt_zigbee_mod import Mqtt_zigbee
from Mqtt_rtl433_mod import Mqtt_rtl433

global main_frame
global sensors


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


def add_row(row, sensor, tempt):
    sensor_frame = ttk.Frame(main_frame, padding = (0, 8, 0, 8),
        style = "Sensor.TFrame")
    sensor_frame.grid(column = 0, row = row, sticky = (E, W))
    sensor_frame.columnconfigure(0, weight = 1, uniform = 1)

    l = ttk.Label(sensor_frame, text = sensor,
        anchor = "center", style = "Sensor.TLabel")
    l.grid(column = 0, row = 0, sticky = (E, W))
    l = ttk.Label(sensor_frame, text = tempt[1], anchor = "center",
        style = "Value.TLabel")
    l.grid(column = 0, row = 1, sticky = (E, W))
    l = ttk.Label(sensor_frame, text = tempt[0], anchor = "center",
        style = "ValueTime.TLabel")
    l.grid(column = 0, row = 2, sticky = (E, W))

    tempt[2] = sensor_frame


def do_run():
    if len(sensors) == 0:
        print("sensors: {}".format(sensors))

    row = 0

    for sensor, tempt in sensors.items():
        print("{}: {}: {} ({})".format(tempt[0], sensor, tempt[1], tempt[2]))

        if tempt[2] is None:
            add_row(row, sensor, tempt)
        else:
            tempt[2].winfo_children()[1]["text"] = tempt[1]
            tempt[2].winfo_children()[2]["text"] = tempt[0]

        row = row + 1

    root.after(15 * 1000, do_run)


if __name__ == '__main__':
    root = Tk();

    root.title("temperatures")

    main_frame = ttk.Frame(root, style = "Main.TFrame")
    main_frame.grid(column = 0, row = 0, sticky = (N, S, E, W))
    main_frame.columnconfigure(0, weight = 1, uniform = 1)

    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)

    sensors = dict()

    mqz = Mqtt_zigbee(sensors)
    mqr = Mqtt_rtl433(sensors)

    set_style()

    root.after(1 * 1000, do_run)

    root.mainloop()
