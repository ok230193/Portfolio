from matplotlib import pyplot as plt
import numpy as np


def plot_numerical_solution():
    y = -1
    h = 0.1
    y_list = []
    x_list = np.arange(0, np.pi * 4, h)
    for x in x_list:
        y = y + h * np.sin(x)
        y_list.append(y)
    return x_list, y_list


def main():
    x, y = plot_numerical_solution()
    print(y)
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
