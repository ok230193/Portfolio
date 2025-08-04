import numpy as np
import matplotlib.pyplot as plt


def cubic_spline_interpolation(x, y):
    h = x[1:] - x[:-1]
    a = y
    left = np.array([[1, 0, 0, 0, 0],
                     [h[0], 2 * (h[0] + h[1]), h[1], 0, 0],
                     [0, h[1], 2 * (h[1] + h[2]), h[2], 0],
                     [0, 0, h[2], 2 * (h[2] + h[3]), h[3]],
                     [0, 0, 0, 0, 1]])
    right = np.array([[0],
                      [3 * (a[2] - a[1]) / h[1] - 3 * (a[1] - a[0]) / h[0]],
                      [3 * (a[3] - a[2]) / h[2] - 3 * (a[2] - a[1]) / h[1]],
                      [3 * (a[4] - a[3]) / h[3] - 3 * (a[3] - a[2]) / h[2]],
                      [0]])
    c = (np.linalg.inv(left) @ right).T[0]
    b = (a[1:] - a[:-1]) / h - h * (c[1:] + 2 * c[:-1]) / 3
    d = (c[1:] - c[:-1]) / (3 * h)
    a = a[:-1]
    c = c[:-1]

    return a, b, c, d


def generate_plot_points(x, a, b, c, d):
    plot_x_array = np.linspace(x[0], x[-1], 50)
    plot_y_array = np.empty(plot_x_array.shape)

    for i in range(len(x) - 1):
        use_indices = (plot_x_array >= x[i]) * (plot_x_array <= x[i+1])
        x_in_range = plot_x_array[use_indices]
        plot_y_array[use_indices] = (a[i] + b[i] * (x_in_range - x[i]) + c[i] * (x_in_range - x[i])**2
                                     + d[i] * (x_in_range - x[i])**3)

    return plot_x_array, plot_y_array


def main():
    x = np.array([0., 1., 4., 5., 8.])
    y = np.array([0., 3., 4., 1., 2.])

    a, b, c, d = cubic_spline_interpolation(x, y)
    plot_x_array, plot_y_array = generate_plot_points(x, a, b, c, d)

    plt.plot(x, y, 'o')
    plt.plot(plot_x_array, plot_y_array)
    plt.show()


if __name__ == '__main__':
    main()
