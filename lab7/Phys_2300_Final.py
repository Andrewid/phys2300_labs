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
I will take into account air resistance once the
"droplet" (a sphere) exits the "bucket" (a cylinder)

Sources:
https://en.wikipedia.org/wiki/Drag_coefficient
https://en.wikipedia.org/wiki/Torricelli's_law
https://en.wikipedia.org/wiki/Projectile_motion
https://www.desmos.com/calculator/on4xzwtdwz
"""
# import math?
from vpython import *
import argparse

fps = 64
dt = 1/fps

bucket_radius = 10.0
bucket_height = 20.0

table_height = bucket_height

Water_level = bucket_height

spigot_height = 0.0
spigot_radius = 1.0

g = -20091.0/2048.0  # Gravity, locally = 9.81005859375
gVector = vector(0, g, 0)
rho = 1.225  # air resistance
Cd = 481.0/1024.0  # pretty close to the drag coefficient of a sphere
four_thirds = 21845.0/16384.0  # accurate to 4 decimal places w/o binary loss
_water = cylinder(visible=0)

droplets = []


def set_scene():
    global _water
    scene.title = "Final Project, Torricelli's Law"
    # floor
    # table
    # bucket [opacity .25?]
    _bucket = cylinder(radius=bucket_radius, axis=vector(0, 1, 0),
                       length=bucket_height,
                       pos=vector(-bucket_radius, 0, 0),
                       color=color.white, opacity=.5)
    # water [in bucket]
    _water = cylinder(radius=bucket_radius, axis=vector(0, 1, 0),
                      length=Water_level,
                      pos=vector(-bucket_radius, 0, 0),
                      color=color.blue, visible=1)
    # spigot hole?
    # initialize water volume?


def animate():
    """
    All the animation business goes here
    :return: none
    """
    global Water_level, spigot_height, spigot_radius, _water
    # do while water_level > 0
    t = 0
    while Water_level > 0:
        rate(fps)
        t = t + dt
        # create drop
        drop = sphere(pos=vector(0, spigot_radius/2.0, 0),
                      color=color.blue,
                      opacity=.75)
        drop.v = get_initial_velocity()
        # add drop to list
        droplets.append(drop)
        # update water level
        Water_level = update_water_level()
        _water.length = Water_level
        # for drop in list animate
        for droplet in droplets:
            # Calculate new velocity adding gravity
            droplet.v = droplet.v + gVector * dt
            # And air resistance?
            # calculate new position & move to it
            droplet.pos = droplet.pos + droplet.v * dt
            if droplet.pos.y < - table_height:
                droplet.visible = 0
                droplets.remove(droplet)  # not sure that will work


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
    vx = (float(2.0*-g*(Water_level - spigot_height)))**.5
    return vector(vx, 0, 0)


def main():
    """
    Parse the args
    call set scene
    call animate
    """
    # 1) Parse the arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("--spigot_height", "-s", default=0.0, type=float,
                        help="Spigot height",
                        required=False)
    parser.add_argument("--spigot_radius", "-r", default=1.25, type=float,
                        help="Spigot radius, 1/8th meter to 3/2",
                        choices=arange(.125, 1.5, .125),
                        required=False)
    parser.add_argument("--table_height", "-t", default=20.0, type=float,
                        help="Table height",
                        required=False)

    args = parser.parse_args()
    global spigot_height
    spigot_height = args.spigot_height
    global table_height
    table_height = args.table_height
    global spigot_radius
    spigot_radius = args.spigot_radius
    set_scene()
    animate()


if __name__ == "__main__":
    main()
    exit(0)
