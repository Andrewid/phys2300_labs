import numpy as np
import pandas as pd  # read_csv()
from vpython import *
import argparse

# globals
Planets = []
G = 1.36*10**-34     # In (au^3/kg*s)
day = 24*60*60.0     # seconds per day
year = 365.25 * day  # seconds per year
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
    # animate(False)
    animate(True)
    # based on their gravitational interactions


def populate_system(file):
    planet_color = 0
    # Add the Sun object
    Planets.append(Planet(mass=1.9891e30, pos=vector(0, 0, 0),
                          vel=vector(0, 0, 0), name='Sun'))
    Planets[planet_color].sphere.color = Colors[planet_color]
    # Parse the CSV, skip line one, make line 2 the header
    planet_data = pd.read_csv(file, skiprows=1)
    for i, row in planet_data.iterrows():
        name = row['planet']
        x0 = float(row[' x(au)'])
        y0 = float(row[' y(au)'])
        vx = float(row[' vx(au/day)'])
        vy = float(row[' vy(au/day)'])
        mass = float(row[' mass(kg)'])
        Planets.append(Planet(mass=mass,
                              pos=vector(x0, y0, 0),
                              vel=vector(vx, vy, 0),
                              name=name))
        if planet_color < (len(Colors) - 1):  # do next, if there is a next
            planet_color += 1
        # Planets[planet_color].sphere.color = Colors[planet_color]


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
    # acc = vector(0, 0, 0)
    t = 0
    dt = day
    time_span = year * 5
    # maybe modify this loop to catch
    # a trigger that goes off once pluto
    # makes a full "year" loop
    while t < time_span:

        rate(500)
        for planet1 in Planets:  # i
            acc = vector(0, 0, 0)
            for planet2 in Planets:  # j
                if planet1 != planet2:
                    # Distance Vector
                    distance = planet2.sphere.pos - planet1.sphere.pos
                    # Magnitude scalar
                    magnitude = distance.mag
                    # magnitude = sqrt((planet2.sphere.pos.x-planet1.sphere.pos.x)**2 +
                    #                  (planet2.sphere.pos.y-planet1.sphere.pos.y)**2)
                    acc += G * planet2.mass * distance / (magnitude**3)

            delta = acc * (dt / leap)
            # only leap once

            planet1.velocity += delta
            planet1.sphere.pos += planet1.velocity * dt
        if leap == 2:  # Change leap only after each planet has been calculated
            leap = 1
        t += dt
    return 1


class Planet(object):
    def __init__(self, **kwargs):

        self.mass = kwargs.get('mass')  # in kg
        self.pos0 = kwargs.get('pos')   # initial position as a vector
        self.velocity = kwargs.get('vel')    # Also a vector
        self.name = kwargs.get('name')  # Planet name
        self.sphere = sphere(pos=self.pos0, radius=radius)  # radius=self.mass*scale?
        self.sphere.make_trail = True


if __name__ == '__main__':
    main()
