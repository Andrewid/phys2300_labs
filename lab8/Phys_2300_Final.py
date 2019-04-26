"""
Final for Andrew Merrell in phys 2300

Torricelli's Law

This physics problem is actually one that I
missed a good amount of points
on my final exam for PHYS 2210
This formula is based of Bernoulli's equation:
ρgy1 + ½ρv12 + P1 = ρgy2 + ½ρv22 +P2

Where the speed of the water dropping is negligible in relation
to the speed of the water exiting the "bucket"

From Wikipedia:
"Torricelli's law describes the parting speed of a jet of water,
based on the distance below the surface at which the jet starts,
assuming no air resistance, viscosity, or other hindrance to the fluid flow. "

I will attempt to reproduce an animated version of this.

Sources:
https://en.wikipedia.org/wiki/Drag_coefficient
https://en.wikipedia.org/wiki/Torricelli's_law
https://en.wikipedia.org/wiki/Projectile_motion
https://www.desmos.com/calculator/on4xzwtdwz
"""
import argparse

# import math?
from vpython import *

fps = 64
dt = 1/fps

bucket_radius = 10.0
bucket_height = 20.0

table_height = bucket_height

Water_level = bucket_height

spigot_height = 0.0
spigot_radius = 1.0

g = -5021.0/512.0  # Gravity "locally" about 9.80665
gVector = vector(0, g, 0)
rho = 1.225  # air resistance
rho_water = 1000  # density of water in kg per meter cubed
Cd = 481.0/1024.0  # pretty close to the drag coefficient of a sphere
four_thirds = 21845.0/16384.0  # accurate to 4 decimal places w/o binary loss
_water = cylinder(visible=0)

droplets = []


def set_scene():
    global _water, spigot_height
    scene.title = "Final Project, Torricelli's Law"
    # floor
    _floor = box(pos=vector(bucket_radius, -table_height, 0),
                 length=bucket_radius*6, width=bucket_radius*3)
    # table
    _table = box(pos=vector(-bucket_radius, -spigot_radius, 0),
                 height=spigot_radius*2,
                 width=bucket_radius*2,
                 length=bucket_radius*2)
    # legs?
    # bucket [opacity .25?]
    _bucket = cylinder(radius=bucket_radius+.125, axis=vector(0, 1, 0),
                       length=bucket_height,
                       pos=vector(-bucket_radius, 0, 0),
                       color=color.white, opacity=.25)
    # water [in bucket]
    _water = cylinder(radius=bucket_radius, axis=vector(0, 1, 0),
                      length=Water_level,
                      pos=vector(-bucket_radius, 0, 0),
                      opacity=.25,
                      color=color.blue, visible=1)
    # spigot hole?
    spigot_height = spigot_height + spigot_radius
    # initialize water volume?


def animate():
    """
    All the animation business goes here
    :return: none
    """
    global Water_level, spigot_height, spigot_radius, _water
    # do while water_level > 0
    t = 0
    # Before getting into this loop let's
    # calculate the air resistance
    # variables since all "drops" are the same
    _drop_area = pi * spigot_radius**2  # cross sectional area of the droplet
    _drop_mass = four_thirds * pi * spigot_radius ** 3 * rho_water
    _alpha = rho * Cd * _drop_area / 2.0
    _beta = _alpha / _drop_mass  # if mass = 1 then _alpha == _beta
    while Water_level > 0 or len(droplets) > 0:
        rate(fps)
        t = t + dt
        # create drop
        if Water_level > 0:
            drop = sphere(pos=vector(0, spigot_height, 0),
                          color=color.blue,
                          opacity=.25,
                          shininess=.7)
            drop.v = get_initial_velocity()
            # add drop to list
            droplets.append(drop)
            # update water level
            Water_level = update_water_level()
            _water.length = Water_level
            # for drop in list animate
        else:
            _water.visible = 0
        for droplet in droplets:
            # Calculate new velocity adding gravity
            droplet.v = droplet.v + gVector * dt
            _speed = droplet.v.mag
            # And air resistance?
            droplet.v -= droplet.v * _speed * _beta * dt
            # calculate new position & move to it
            droplet.pos = droplet.pos + droplet.v * dt
            if droplet.pos.y < - table_height:
                droplet.visible = 0
                droplets.remove(droplet)  # not sure that will work
        print(Water_level, len(droplets))
    print("All done!")


def update_water_level():
    """
    every time we instantiate a new water droplet we recalculate water_level
    Vi = pi*R*R*H    # volume of water currently
    v = 4/3*pi*r**3  # volume of droplet
    Vn = Vi - v      # subtract volume of droplet from volume of water
    H = Vn/pi*R**2   # new volume divided by pi times R squared
    The pi's cancel...
    :return:  new water_level
    """
    # Simplify a little bit
    global Water_level, four_thirds, spigot_radius, bucket_radius
    return ((bucket_radius**2 * Water_level    # Vi/pi
            - four_thirds * spigot_radius**3)  # v/pi
            / bucket_radius**2)                # pi*H


def get_initial_velocity():
    """
    Using the following to calculate initial velocity of water droplet
    water_level, bucket_radius, spigot_height, spigot_radius
    :return: a velocity vector
    """
    global Water_level, spigot_height
    vx = (float(2.0*-g*(Water_level - spigot_height + spigot_radius)))**.5
    return vector(vx, 0, 0)


def main():
    """
    Parse the args
    call set scene
    call animate
    """
    # 1) Parse the arguments
    """ parser.add_argument("--spigot_height", "-s", default=0.0, type=float,
                         help="Spigot height",
                         required=False)
     Changing spigot height from 0 will require moving the _water
     up to the spigot height and adding another "useless"
     cylinder of water, that never empties.
                         """
    parser = argparse.ArgumentParser()
    global bucket_radius, bucket_height, table_height, spigot_radius
    parser.add_argument("--bucket_height", "-b", default=20.0, type=float,
                        choices=arange(10, 40, 5),
                        help="Bucket height",
                        required=False)

    parser.add_argument("--bucket_radius", "-br", default=10.0, type=float,
                        choices=arange(5, 20, 5),
                        help="Bucket_radius",
                        required=False)

    parser.add_argument("--spigot_radius", "-r", default=1, type=float,
                        help="Spigot radius, 1/8th meter to 3/2",
                        choices=arange(.25, 2, .125),
                        required=False)
    parser.add_argument("--table_height", "-t", default=20.0, type=float,
                        help="Table height",
                        required=False)

    args = parser.parse_args()
    bucket_radius = args.bucket_radius
    bucket_height = args.bucket_height
    table_height = args.table_height
    spigot_radius = args.spigot_radius
    set_scene()
    animate()


if __name__ == "__main__":
    main()
    exit(0)
