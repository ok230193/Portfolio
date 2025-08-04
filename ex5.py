import matplotlib.pyplot as plt


def f(x):
    return 6 * x ** 4 + 7 * x ** 3 - 127 * x ** 2 - 266 * x - 120


def df(x):
    return 24 * x ** 3 + 21 * x ** 2 - 254 * x - 266


def main():
    x0 = 8
    e = 0.00001
    x_list = [x0]

    while True:
        x1 = x0 - (f(x0) / df(x0))
        x_list.append(x1)

        if abs(x1 - x0) < e:
            break
        x0 = x1

    print(x_list[-1])


if __name__ == '__main__':
    main()
