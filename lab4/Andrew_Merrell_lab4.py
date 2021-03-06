"""
Assignment to learn how to interpolate data1
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd
from datetime import datetime as dt
import dateutil


# https://youtu.be/-zvHQXnBO6c
def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    _df = pd.read_csv(wx_file)

    _time0 = None
    previous_temp = 0.0
    harbor_data['Debug'] = []
    harbor_data['wx_times'] = []
    harbor_data['wx_temperatures'] = []
    # Stop recording values if the "mission time" for the altitude has elapsed?
    end_mission = harbor_data['gps_times'][-1]
    for _index, row in _df.iterrows():
        time, temp = row['Time'], row['Ch1:Deg F']
        # discard bad data
        if temp < -99:
            continue

        if not _time0:
            previous_temp = temp
            _time0 = dt.strptime(time, '%H:%M:%S')

        _time = dt.strptime(time, '%H:%M:%S')
        _seconds = (_time - _time0).total_seconds()  # Delta
        _hours = _seconds / 3600

        # This should bail out from recording hours beyond what's needed
        if not _hours < end_mission:
            break

        pct_change = pct_diff(temp, previous_temp)
        harbor_data['Debug'].append(pct_change)
        # smooth out data??
        if temp - previous_temp > 2.7:  # if pct_change > .5:??

            # how do I get the next temperature for averaging?
            temp = previous_temp  # Average the adjacent temps?

        harbor_data['wx_times'].append(_hours)
        harbor_data['wx_temperatures'].append(temp)
        previous_temp = temp
    return 0


def pct_diff(a, b):
    """
    calculate a percentage of change from one number to the other
    :param a: any number
    :param b: any number
    :return:  the % of change
    """
    a = abs(a)
    b = abs(b)
    if a > b:
        return (a - b) / a
    else:
        return (b - a) / b


def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists:
                                gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """

    harbor_data['gps_times'] = []
    harbor_data['gps_altitude'] = []
    headers = ['hour', 'minute', 'second', 'met', 'long', 'lat', 'altitude']
    _df = pd.read_csv(gps_file, sep='\t', names=headers, skiprows=[1], header=0)
    # note, the second row is dashes
    _time0 = None
    for _index, row in _df.iterrows():
        hour = row['hour']
        minute = row['minute']
        second = row['second']
        altitude = row['altitude']
        _time = dateutil.parser.parse('{}:{}:{}'.format(hour, minute, second))

        if not _time0:
            _time0 = _time

        # hours elapsed since _time0
        hours_elapsed = (_time - _time0).total_seconds() / 3600
        harbor_data['gps_times'].append(hours_elapsed)
        harbor_data['gps_altitude'].append(altitude)
    return 0


def get_slope_intercept(x1, y1, x2, y2):
    """
    get the slope and y intercept of a line based on 2 pairs of coordinates
    :param x1: initial x coord
    :param y1: initial y coord
    :param x2: second x coord
    :param y2: second y coord
    :return: the slope between the 2 points
    """
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    harbor_data["altitude_up"] = []
    harbor_data["temperature_up"] = []
    harbor_data["altitude_down"] = []
    harbor_data["temperature_down"] = []
    temps = len(harbor_data["wx_temperatures"])
    gps_times = len(harbor_data['gps_times'])
    wx_index = 0
    for i, gps_time_delta in enumerate(harbor_data['gps_times']):
        if not i + 1 < gps_times:
            break
        if not wx_index < temps:
            break
        altitude = harbor_data["gps_altitude"][i]
        gps_next_time_delta = harbor_data['gps_times'][i + 1]
        next_altitude = harbor_data["gps_altitude"][i + 1]

        wx_time_delta = harbor_data['wx_times'][wx_index]

        while gps_next_time_delta > wx_time_delta:

            # interpolate
            slope, intercept = get_slope_intercept(gps_time_delta,  # x1
                                                   altitude,  # y1
                                                   gps_next_time_delta,  # x2
                                                   next_altitude)  # y2
            # check for index out of range and break if so?
            if not temps > wx_index:
                break
            wx_temp = harbor_data["wx_temperatures"][wx_index]
            interp_altitude = slope * wx_time_delta + intercept

            # Decide where to put the data based on if we're descending or not
            if altitude < next_altitude:
                # ascending
                harbor_data["altitude_up"].append(interp_altitude)
                harbor_data["temperature_up"].append(wx_temp)

            else:
                # descending
                harbor_data["altitude_down"].append(interp_altitude)
                harbor_data["temperature_down"].append(wx_temp)

            # update new time delta for weather
            wx_time_delta = harbor_data['wx_times'][wx_index]
            # then increment weather index
            wx_index += 1
        # if I got here then I need to go to the next delta time in gps times

    return 0


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    plt.figure()
    plt.subplot(2, 1, 1)  # select first subplot
    plt.title("Harbor Flight Data")
    plt.plot(harbor_data['wx_times'], harbor_data['wx_temperatures'])
    plt.xlabel("Mission Elapsed Time. Hours")
    plt.ylabel("Temperature, F")

    plt.subplot(2, 1, 2)
    plt.plot(harbor_data['gps_times'], harbor_data['gps_altitude'])
    plt.xlabel("Mission Elapsed Time. Hours")
    plt.ylabel("Altitude")

    plt.show()

    plt.figure()
    plt.subplot(1, 2, 1)  # select first subplot
    plt.title("Harbor Ascent Flight Data")
    plt.plot(harbor_data["temperature_up"],
             harbor_data["altitude_up"])
    plt.xlabel("Temperature, F")
    plt.ylabel("Altitude, Feet")

    plt.subplot(1, 2, 2)
    plt.title("Harbor Descent Flight Data")
    plt.plot(harbor_data["temperature_down"],
             harbor_data["altitude_down"])
    plt.xlabel("Temperature, F")
    plt.ylabel("Altitude, Feet")

    plt.show()

    plt.figure()
    plt.plot(harbor_data["wx_times"], harbor_data['Debug'])
    plt.show()


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    # first program input param
    # wx_file = sys.argv[1]
    wx_file = "TempPressure.txt"
    # second program input param
    # gps_file = sys.argv[2]
    gps_file = "GPSData.txt"

    read_gps_data(gps_file, harbor_data)  # collect gps data
    read_wx_data(wx_file, harbor_data)  # collect weather data

    interpolate_wx_from_gps(harbor_data)  # calculate interpolated data
    plot_figs(harbor_data)  # display figures


if __name__ == '__main__':
    main()
    exit(0)
