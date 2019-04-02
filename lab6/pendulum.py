import numpy as np
from matplotlib import pyplot as plt
from vpython import scene, cylinder, sphere, box, vector

gravity = 9.81    # m/s**2
length = 0.1     # meters
width = 0.002   # arm radius
radius = 0.01    # ball radius
frame_rate = 100
steps_per_frame = 10

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
    scene.forward = vector(0, -.3, -1)
    scene.x = -1


def f_theta_omega(angles, resistance=0.0):  # t isn't necessary, is it?
    """

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
    rate = 1.0/(frame_rate * steps_per_frame)  # Size of single step
    angles = np.array([np.pi*90/180, 0], float)
    theta = []  # An array of angles
    tpoints = np.arange(0, 10, rate)

    for t in tpoints:
        theta.append(angles[0] * (180.0 / np.pi))
        k1 = rate * f_theta_omega(angles)
        k2 = rate * f_theta_omega(angles + 0.5 * k1)
        k3 = rate * f_theta_omega(angles + 0.5 * k2)
        k4 = rate * f_theta_omega(angles + k3)
        angles += (k1+2*k2+2*k3+k4)/6

    plt.plot(tpoints, theta)
    plt.xlabel("time")
    plt.ylabel("Angle")
    plt.show()
    # Task 2
    set_scene()
    # Initial x and y
    x = length * np.sin(angles[0])
    y = -length * np.cos(angles[0])
    _pos = vector(x, y, 0)  #initialize _position
    set_scene()
    _ceiling = box(pos=vector(length, 2*length, 0), height=radius,
                   width=radius, length=2*length)

    bob = sphere()
    rope = cylinder()
    # Use the 4'th order Runga-Kutta approximation
    for i in range(steps_per_frame):
        angles += rate * f_theta_omega(angles)

        t += rate
        # Update positions
        x = length * np.sin(angles[0])
        y = -length * np.cos(angles[0])

        bob.pos = vector(x, y, 0)
        rope.axis = bob.pos  # axis points towards the bob

    # Task 3
    theta_d = []  # New array of angles for the function with drag
    drag = .3
    for t in tpoints:
        theta_d.append(angles[0] * (180.0 / np.pi))
        k1 = rate * f_theta_omega(angles, drag)
        k2 = rate * f_theta_omega(angles + 0.5 * k1, drag)
        k3 = rate * f_theta_omega(angles + 0.5 * k2, drag)
        k4 = rate * f_theta_omega(angles + k3, drag)
        angles += (k1+2*k2+2*k3+k4)/6

    plt.plot(tpoints, theta_d)
    plt.xlabel("time")
    plt.ylabel("Angle")
    plt.show()

if __name__ == "__main__":
    main()
    exit(0)
