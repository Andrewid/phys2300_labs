"""
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
"""

import sys
import matplotlib.pylab as plt
import numpy as np


# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into int years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third [2] column (date)
                        One list with the information from the fourth [3] column (temperature)
    """
    wdates = []  # list of dates data
    wtemperatures = []  # list of temperature data
    # TODO: Extract the data from in-file as csv
    with open(infile) as f_in:
        next(f_in)          # Does this actually dump the first line?
        for line in f_in:
            _fields = line.split()
            if _fields[3] != '999.9':
                wdates.append(_fields[2])                  # full date strings, for now?
                wtemperatures.append(float(_fields[3]))    # temps converted to floats
    return wdates, wtemperatures


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    if len(wdates) != len(wtemp):
        print('Lists must be of equal length')
        return -1
    means = [None] * 12        # 0 for January
    std_dev = [None] * 12      # up to 11 for December
    # create a dict of months with a temperature list for each to then calculate
    _months = {}
    for offset in range(len(wdates)):
        _month = int(wdates[offset][4:6])  # get just the month part of the data in dates list
        if _month in _months:
            _months[_month].append(float(wtemp[offset]))
        else:
            _months[_month] = []
            _months[_month].append(float(wtemp[offset]))

    for month in _months:
        std_dev[month-1] = np.std(_months[month])
        means[month-1] = np.mean(_months[month])
    return means, std_dev

def calc_min_max(wdates, wtemp):
    """
    Taking in date strings and temperatures, combining the data into
    dictionaries for each year, with a list of all temperatures for values
    using standard min and max functions of lists to create the needed lists
    :param wdates: 8 char list of date data in 'yyyymmdd' format
    :param wtemp:  list of temperatures
    :return: lists of the minimum and maximum temperatures per year and the years in question
            -1 if passed in lists are not of equal length
    """
    if len(wdates) != len(wtemp):
        print('Lists must be of equal length')
        return -1

    # create a dict of years with a temperature list for each to then calculate
    _years = {}
    for offset in range(len(wdates)):
        _year = int(wdates[offset][:4])  # get just the year part of the data in dates list
        if _year in _years:
            _years[_year].append(float(wtemp[offset]))
        else:
            _years[_year] = []
            _years[_year].append(float(wtemp[offset]))
    num_years = len(_years)

    t_min = [None] * num_years
    t_max = [None] * num_years
    l_years = [None] * num_years
    offset = 0
    for year in _years:  # We're making a terrible assumption that the years are in order
        t_min[offset] = np.min(_years[year])
        t_max[offset] = np.max(_years[year])
        l_years[offset] = year
        offset += 1
    return t_min, t_max, l_years

def plot_data_task1(dates, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per

    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    int_year = []  # empty list to fill with parsed year data
    for s_date in dates:
        int_year.append(int(s_date[:4]))  # Just give me the first four chars, as an int

    plt.figure()
    plt.subplot(2, 1, 1)  # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(int_year, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Int Year")

    plt.subplot(2, 1, 2)  # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber,
            month_mean,
            yerr=month_std,
            width=width,
            color="lightgreen",
            ecolor="black",
            linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()  # display plot


def plot_data_task2(t_min, t_max, years):
    """
    Plot the min an max temperatures per year we have valid records
    :param t_min: list of minimum temps for the years
    :param t_max: list of maximum temps for the years
    :param years: Years in question
    :return: -1 if passed in lists have unequal length
    """
    expected_length = len(years)
    if (expected_length != len(t_max)) | (expected_length != len(t_min)):
        return -1
    plt.figure()

    plt.plot(years, t_max, 'ro', label='Maximum Temperature')
    plt.plot(years, t_min, 'bo', label='Minimum Temperature')
    plt.legend()
    plt.ylabel("Temperature, F")
    plt.xlabel("Int Year")
    plt.show()


def main(infile):
    weather_data = infile  # take data file as input parameter to file
    wdates, wtemperatures = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    plot_data_task1(wdates, wtemperatures, month_mean, month_std)
    # TODO: Create the data you need for this
    # calc_min_max conveniently returns exactly what plot_data_task2 requires
    t_min, t_max, years = calc_min_max(wdates, wtemperatures)
    plot_data_task2(t_min, t_max, years)


if __name__ == "__main__":
    infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    # infile = sys.argv[1]
    main(infile)
    exit(0)
