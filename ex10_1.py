import numpy as np
import matplotlib.pyplot as plt


def lagrange_interpolation(points, x):
    interpolated_point = 0
    for j in range(4):
        dev = 1
        for i in range(4):
            if i != j:
                dev *= (x - points[i, 0]) / (points[j, 0] - points[i, 0])
        interpolated_point += dev * points[j, 1]

    return interpolated_point


def main():
    points = np.array([[0, 1], [1, 3], [2, 3], [3, 5]])

    x = np.linspace(0, 3, 100)
    y = np.empty(x.shape)

    for idx in range(len(x)):
        y[idx] = lagrange_interpolation(points, x[idx])

    plt.plot(x, y)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.show()


if __name__ == '__main__':
    main()
