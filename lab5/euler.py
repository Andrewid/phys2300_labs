import numpy as np

def f_x(x, t):
    """

    :param x:
    :param t:
    :return:
    """
    return -x**3 + np.sin(t)

def main():
    """

    :return:
    """
    a = 0.0
    b = 10.0
    N = 1000
    h = (b-a)/N = 0.0

    tpoints = np.arange(a, b, h)
    xpoints = []

    for t in tpoints:
        xpoints.append(x)
        x += h*f_x(x, t)

    print(xpoints)

if __name__ == "__main__":
    main()
    exit(0)
