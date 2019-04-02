import numpy as np
from matplotlib import pyplot as plt
from vpython import scene, cylinder, sphere, box, vector, rate, color

gravity = 9.81    # m/s**2
length = 0.1     # meters
width = 0.002   # arm radius
radius = 0.01    # ball radius
frame_rate = 200
steps_per_frame = 3

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 6: Simple pendulum"
    scene.width = 800
    scene.height = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, 2.5, -5)
    scene.x = -1
    rate(frame_rate)


def f_theta_omega(angles, resistance=0.0):  # t isn't necessary, is it?
    """
    Gives us the next two angles for a pendulum in motion
    :param angles: a two piece array containing theta and omega
    :param resistance: Optional resistance
    :return:
    """
    # r is an array of 2 values theta and omega
    if len(angles) < 2:
        return -1
    theta = angles[0]
    omega = angles[1]
    ftheta = omega
    fomega = -(gravity/length) * np.sin(theta) - (resistance * omega)
    return np.array([ftheta, fomega], float)


def main():
    """
    """
    # Task 1 & some of task 2
    # Set up initial values
    r = 1.0/(frame_rate * steps_per_frame)  # Size of single step
    angles = np.array([np.pi*55/180, 0], float)
    theta = []  # An array of angles
    tpoints = np.arange(0, 20, r)

    # Use the 4'th order Runga-Kutta approximation
    for t in tpoints:
        theta.append(angles[0] * (180.0 / np.pi))
        k1 = r * f_theta_omega(angles)
        k2 = r * f_theta_omega(angles + 0.5 * k1)
        k3 = r * f_theta_omega(angles + 0.5 * k2)
        k4 = r * f_theta_omega(angles + k3)
        angles += (k1+2*k2+2*k3+k4)/6

    plt.plot(tpoints, theta)
    plt.xlabel("time")
    plt.ylabel("Angle")
    plt.show()

    # Task 2
    # Initial x and y
    x = np.sin(angles[0] * (180.0 / np.pi))
    y = np.cos(angles[0] * (180.0 / np.pi))
    _pos = length * vector(x, -y, 0)  # initialize _position
    set_scene()
    _ceiling = box(pos=vector(0, 0, 0), height=radius,
                   width=2*length, length=2*length,
                   color=color.green)

    bob = sphere(radius=radius, pos=_pos, color=color.blue)
    rope = cylinder(length=length, radius=width, axis=_pos, color=color.orange)

    for angle in theta:
        rate(frame_rate)
        angle = np.radians(angle)
        # Update positions
        x = length * np.sin(angle)
        y = -length * np.cos(angle)
        
        bob.pos = vector(x, y, 0)
        rope.axis = bob.pos  # axis points towards the bob

    # Task 3
    theta_d = []  # New array of angles for the function with drag
    drag = .3
    for t in tpoints:
        theta_d.append(angles[0] * (180.0 / np.pi))
        k1 = r * f_theta_omega(angles, drag)
        k2 = r * f_theta_omega(angles + 0.5 * k1, drag)
        k3 = r * f_theta_omega(angles + 0.5 * k2, drag)
        k4 = r * f_theta_omega(angles + k3, drag)
        angles += (k1+2*k2+2*k3+k4)/6

    plt.plot(tpoints, theta_d)
    plt.xlabel("time")
    plt.ylabel("Angle")
    plt.show()

    for angle in theta_d:
        rate(frame_rate)
        angle = np.radians(angle)
        # Update positions
        x = length * np.sin(angle)
        y = -length * np.cos(angle)

        bob.pos = vector(x, y, 0)
        rope.axis = bob.pos  # axis points towards the bob


if __name__ == "__main__":
    main()
    exit(0)
