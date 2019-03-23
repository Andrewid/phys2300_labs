"""
Homework #2
For PHYS 2300 with Dr. Hugo Valle
Andrew Merrell      02-04-2019

"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

# NOTE: You may need to run: $ pip install matplotlib

# Function to calculate projectile motion

def projectile_motion(initial_position, velocity, time, acceleration):
    """
    Take in the initial position, time, velocity, and acceleration
    give back final position based on calculation below
    :param initial_position:    Initial position canbe x, y, or even z
    :param velocity:            velocity of object
    :param time:                time to calculate change of position
    :param acceleration:        acceleration or deceleration to apply
    :return:                    returns 1 dimensional final position based on inputs
    """
    return initial_position + velocity * time + (acceleration*time*time)/2

def two_dimensional_motion(x_initial,
                           y_initial,
                           x_velocity,
                           y_velocity,
                           x_acceleration,
                           y_acceleration,
                           delt, t):
    """

    :param x_initial:       Initial position of object on x axis
    :param y_initial:       Initial position of object on y axis
    :param x_velocity:      Velocity of object moving along x
    :param y_velocity:      Velocity of object moving along y
    :param x_acceleration:  Acceleration of object on x
    :param y_acceleration:  Acceleration of object on y (usually gravity)
    :param delt:            Change in time
    :param t:               Time elapsed
    # could have made an array of tuples...
    :return:                Returns a tuple of arrays containing x and y coordinates
    """
    _x_coordinates = []
    _y_coordinates = []
    _this_x = 0.0
    _this_y = 0.0

    while True:
        _this_y = projectile_motion(y_initial,
                                    y_velocity,
                                    t,
                                    y_acceleration)
        if (0.0 > _this_y):
            break
        _y_coordinates.append(_this_y)
        _this_x = projectile_motion(x_initial,
                                    x_velocity,
                                    t,
                                    x_acceleration)
        _x_coordinates.append(_this_x)

        t = t + delt
    #TODO: figure out where the final y would come to 0 and and add an x,y final spot
    return _x_coordinates, _y_coordinates # a tuple of arrays


# Function to plot data
def plot_data(x, y, xlabel = 'x', ylabel ='y'):
    """
    passing in two (float) arrays and displaying what ought to be an arc
    :param x: Array of x positions
    :param y: Array of y positions
    :param xlabel:
    :param ylabel:
    :return: 0 if no error
    """
    plt.plot(x, y)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    return 0

# "Main" Function
def main():
    """
    Ask for input
    run the calculation
    display results

    :return: 0 if no error
    """

    x_coordinates = []
    y_coordinates = []

    # gravity is -9.8m/s
    ax =  0.0   # no sideways gravity
    ay = -9.8   # define gravity 

    delt = 0.1  # change in time
    t    = 0.0  # initial time

    # Consider braking this to an input function
    # allow each to loop unit proper data is input
    # TODO: error handling if not input NAN
    x0  = input("Initial x coordinate: ")   or 1.0
    vx0 = input("Initial x velocity m/s: ") or 70.0

    y0  = input("Initial y coordinate: ")   or 0.0
    vy0 = input("Initial y velocity m/s: ") or 80.0

    # pass x & y arrays to function?
    # have function just pass 2 arrays back? 
    x_coordinates, y_coordinates = two_dimensional_motion(x0, y0, vx0, vy0, ax, ay, delt,t)
    
    # plot & display
    plot_data(x_coordinates, y_coordinates, 'Position of x over time', 'height')

#check if name == __main__
if __name__ == "__main__":
    main()
    exit(0)
