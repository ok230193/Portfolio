import numpy as np
from matplotlib import pyplot as plt


def f(x):
    M = 6.0 * 10 ** 24
    G = 6.67 * 10 ** -11
    r = np.linalg.norm(x)
    return -G * M * x / r ** 3


def main():
    t_max = 86400
    h = 60
    t = 0
    x = np.array([0, 4.23 * 10 ** 7])
    v = np.array([3000, 0])
    x_list = [x]

    while t < t_max:
        k1 = h * v
        l1 = h * f(x)
        k2 = h * (v + l1 / 2)
        l2 = h * f(x + k1 / 2)
        k3 = h * (v + l2 / 2)
        l3 = h * f(x + k2 / 2)
        k4 = h * (v + l3)
        l4 = h * f(x + k3)
        x = x + (k1 + 2 * (k2 + k3) + k4) / 6
        v = v + (l1 + 2 * (l2 + l3) + l4) / 6
        x_list.append(x)
        t += h
    x_array = np.array(x_list)
    plt.plot(x_array[:, 0], x_array[:, 1])
    plt.show()


if __name__ == '__main__':
    main()
