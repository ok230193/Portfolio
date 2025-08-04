import numpy as np


def trapezoidal_rule(a, b, n):
    y = 0
    x = np.linspace(a, b, n + 1)
    for i in range(n):
        y += (np.sin(x[i + 1]) + np.sin(x[i])) * (b - a) / n / 2

    return y


def main():
    a = 0
    b = np.pi
    n = 100
    y = trapezoidal_rule(a, b, n)
    print(y)


if __name__ == '__main__':
    main()
