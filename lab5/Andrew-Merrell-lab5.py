from vpython import *
from math import sin, cos
import argparse


def set_scene(data):
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.height = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(-25, data['init_height'], 0),
                     radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position

    # Animate & store
    data["x1"] = []
    data["y1"] = []
    y0 = data["init_height"]
    x0 = 0
    x, y = 0, 0
    ball_nd.pos = (x, y, 0)
    dt = .1
    t = 0
    vx0 = data['init_velocity'] * cos(radians(data['theta']))
    vy0 = data['init_velocity'] * sin(radians(data['theta']))
    while y >= 0:
        rate(1000)
        data["x1"].append(x)
        data["y1"].append(y)
        ball_nd.pos = vector(x, y, 0)
        t = t + dt
        x = x0 + vx0 * t
        y = y0 + vy0 * t + (data['gravity']/2) * (t**2)


def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    """
    ball_wd = sphere(pos=vector(-25, data['init_height'], 0),
                     radius=1, color=color.red, make_trail=True)
    scene.camera.follow(ball_wd)

    data["x2"] = []
    data["x2"] = []
    pass


def main():
    """
    """
    # 1) Parse the arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("--height", "-y", default="1.2", type=float,
                        help="Position on the Y axis to start",
                        required=False)
    parser.add_argument("--velocity", "-v", default='5', type=float,
                        help="Velocity in m/s",
                        required=False)
    parser.add_argument("--angle", "-a", default='45', type=float,
                        help="Angle in degrees (will be converted)",
                        required=False)

    args = parser.parse_args()
    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = args.height       # y-axis
    data['init_velocity'] = args.velocity   # m/s
    data['theta'] = args.angle              # degrees
    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.81  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
#    motion_drag(data)
    # 4) Plot Information: extra credit
#    plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
