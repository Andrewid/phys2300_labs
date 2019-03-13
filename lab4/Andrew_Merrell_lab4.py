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
    harbor_data['wx_times'] = []
    harbor_data['wx_temperatures'] = []

    for index, row in _df.iterrows():
        time, temp = row['Time'], row['Ch1:Deg F']
        if temp < -99:
            continue
        if not _time0:
            previous_temp = temp
            _time0 = dt.strptime(time, '%H:%M:%S')

        # smooth out data??
        if 0 > temp > -13 and temp - previous_temp > 3:
            temp = _df[index-1]['Ch1:Deg F'] + _df[index+1]['Ch1:Deg F'] / 2  # Average the adjacent temps
        _time = dt.strptime(time, '%H:%M:%S')
        _seconds = (_time - _time0).total_seconds()  # Delta
        _hours = _seconds/3600
        harbor_data['wx_times'].append(_hours)
        harbor_data['wx_temperatures'].append(temp)

    return 0


def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
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
    for index, row in _df.iterrows():
        hour = row['hour']
        minute = row['minute']
        second = row['second']
        altitude = row['altitude']

        if not _time0:
            _time0 = dateutil.parser.parse('{}:{}:{}'.format(hour, minute, second))

        _time = dateutil.parser.parse('{}:{}:{}'.format(hour, minute, second))
        harbor_data['gps_times'].append((_time - _time0).total_seconds()/3600)  # hours elapsed since _time0
        harbor_data['gps_altitude'].append(altitude)
    return 0


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

    pass


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    pass


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

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data

    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)
