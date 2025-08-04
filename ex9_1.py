import numpy as np


def monte_carlo_pi():
    pattern_max = 300000
    np.random.seed(0)
    match = 0

    for i in range(pattern_max):
        x = np.random.random()
        y = np.random.random()

        if x ** 2 + y ** 2 <= 1:
            match += 1

    pi = (4 * match) / pattern_max

    return pi


def main():
    pi = monte_carlo_pi()
    print(f'{pi}')



if __name__ == '__main__':
    main()
