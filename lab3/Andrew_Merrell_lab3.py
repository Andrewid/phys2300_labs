'''
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
'''
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
#       convert year, month, day into decimal years for plotting
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
                wdates.append(_fields[2])                  # strings, for now
                wtemperatures.append(float(_fields[3]))    # convert to float
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
    for key, value in enumerate(wdates):
        _month = int(value[4:6])
        if _month in _months:
            _months[month].append(float(wtemp[key]))
        else:
            _months[month] = []
            _months[month].append(float(wtemp[key]))
    # _months.sort() # j/k Dictionaries can't be sorted

    for month in _months:
        std_dev[month-1] = np.std(_months[month])
        means[month-1] = np.mean(_months[month])
    return means, std_dev


def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per

    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)  # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")

    plt.subplot(2, 1, 2)  # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, year=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()  # display plot


def plot_data_task2(wdates, wtemperatures):
    """

    :param wdates:
    :param wtemperatures:
    :return:
    """
    pass


def main(infile):
    weather_data = infile  # take data file as input parameter to file
    wdates, wtemperatures = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    plot_data_task1(wdates, wtemperatures, month_mean, month_std)
    # TODO: Create the data you need for this
    # plot_data_task2(xxx)


if __name__ == "__main__":
    infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    # infile = sys.argv[1]
    main(infile)
    exit(0)
