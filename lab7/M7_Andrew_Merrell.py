"""
This program attempts  to model the
solar system and animate the bodies based on
their initial positions, velocity vectors and masses
and calculates their positions based on the gravitational
forces each body has on every other body. (including the Sun)

-Andrew Merrell
for Physics 2300
Dr. Hugo Valle
"""
from vpython import *
import numpy as np
import pandas as pd  # read_csv()
import argparse

# globals
System = []
G = 1.36*10**-34     # In (au^3/kg*s)
radius = .0125

light_blue = color.blue + color.white
Colors = [color.yellow,    # Sun
          color.gray(80),  # Mercury
          color.cyan,      # Venus
          color.blue,      # Earth
          color.red,       # Mars
          color.orange,    # Jupiter
          color.magenta,   # Saturn
          light_blue,      # Uranus
          light_blue,      # Neptune
          color.orange]    # Pluto


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--File", "-f", default="solar_system_points.csv",
                        help="File with positions and velocities of planets"
                        )
    args = parser.parse_args()
    file = args.File
    # call function to populate a list of planet objects extracted from the csv file
    populate_system(file)
    # an animation loop calculating the planet's next position
    # animate(False)  # Uncomment for task 1
    animate(True)  # True if we do want the leap frog method
    # based on their gravitational interactions


def populate_system(file):
    planet_color = 0
    # Add the Sun object
    System.append(Planet(mass=1.9891e30, pos0=vector(0, 0, 0),
                         vel=vector(0, 0, 0), name='Sun'
                         ))
    System[planet_color].sphere.color = Colors[planet_color]
    System[planet_color].sphere.trail_color = color.yellow
    # Parse the CSV, skip line one, make line 2 the header
    planet_data = pd.read_csv(file, skiprows=1)
    for i, row in planet_data.iterrows():
        name = row['planet']
        x0 = float(row[' x(au)'])
        y0 = float(row[' y(au)'])
        vx = float(row[' vx(au/day)'])
        vy = float(row[' vy(au/day)'])
        mass = float(row[' mass(kg)'])
        System.append(Planet(mass=mass,
                             pos0=vector(x0, y0, 0),
                             vel=vector(vx, vy, 0),
                             name=name))
        if planet_color < (len(Colors) - 1):  # do next, if there is a next
            planet_color += 1
        System[planet_color].sphere.color = Colors[planet_color]
        System[planet_color].sphere.trail_color = Colors[planet_color]

    # Asteroid loop here


def animate(leapfrog):
    """
    Change planetary positions due to the
    gravitational effect of other objects
    :param leapfrog: True if using the leapfrog method
    :return: 1 if ok
    """
    leap = 1
    if leapfrog:
        leap = 2
    t = 0
    dt = .5  # not day

    while True:
        rate(2400)  #
        for body1 in System:  # i
            acc = vector(0, 0, 0)
            for body2 in System:  # j
                # We can have a bunch of "asteroid" objects
                # and they won't interact with each other
                if body1.name == body2.name:
                    continue
                distance = body2.sphere.pos - body1.sphere.pos  # Distance Vector
                magnitude = distance.mag  # Magnitude scalar
                acc += G * body2.mass * distance / (magnitude**3)

            delta = acc * (dt / leap)
            body1.velocity += delta
            body1.sphere.pos += body1.velocity * dt
        if leap == 2:  # Change leap only after each planet has been calculated
            leap = 1
        t += dt
        # if t % (248*365) == 0:  # pluto takes about 248 earth years to orbit
        #     print(t)
    return 1


class Planet(object):
    # Why not just a sphere object that gains
    # a Velocity vector a
    # Mass and a Name?
    def __init__(self, **kwargs):

        self.mass = kwargs.get('mass')  # in kg
        self.pos0 = kwargs.get('pos0')   # initial position as a vector
        self.velocity = kwargs.get('vel')    # Also a vector
        self.name = kwargs.get('name')  # Planet name
        self.sphere = sphere(pos=self.pos0,
                             make_trail=True,
                             radius=radius  # constant of .0125
                             )  # move it before making trail?
        # if "Earth" in self.name:
        #     self.sphere.material = materials.earth



if __name__ == '__main__':
    main()
