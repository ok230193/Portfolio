import matplotlib.pyplot as plt
import math

import numpy as np


def y(x):
    return x ** 3 - 6 * x ** 2 + x + 10


def main():
    xd = np.linspace(0, 10, 100)

    h = 0.01

    fd = (y(xd + h) - y(xd - h)) / (2 * h)

    plt.plot(xd, fd)
    plt.show()


if __name__ == '__main__':
    main()
