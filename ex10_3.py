import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x**2-4*x+4


def calc_a(x_data, k, j):
    a = 0
    for x in x_data:
        a += x ** (k + j)
    return a


def calc_b(x_data, y_data, k):
    b = 0
    for x, y in zip(x_data, y_data):
        b += y * x ** k
    return b


def least_squares_method(x_data, y_data):
    alpha = np.empty((3, 3))
    beta = np.empty((3, 1))
    for k in range(3):
        beta[k] = calc_b(x_data, y_data, k)
        for j in range(3):
            alpha[k, j] = calc_a(x_data, k, j)

    c = np.linalg.inv(alpha) @ beta
    return c


def main():
    np.random.seed(0)
    x_data = np.linspace(-3, 7, 100)
    y_data = f(x_data) + np.random.uniform(-1, 1, x_data.shape)

    c = least_squares_method(x_data, y_data)

    plt.plot(x_data, c[2]*x_data**2+c[1]*x_data+c[0])
    plt.plot(x_data, y_data, 'o')
    plt.show()


if __name__ == '__main__':
    main()
