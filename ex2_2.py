import math


def quadratic_formula(a, b, c):
    x_1 = 2 * c / (-b - math.sqrt(b * b - 4 * a * c))
    x_2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return x_1, x_2


def main():
    a = 1.0
    b = 1000.001
    c = 1.0
    x_1, x_2 = quadratic_formula(a, b, c)
    print(x_1)
    print(x_2)


if __name__ == '__main__':
    main()
