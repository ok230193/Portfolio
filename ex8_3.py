import random
import numpy as np


def monte_carlo_integration(a, b, n):
    ans = 0
    for i in range(n):
        x = random.uniform(a, b)
        y = np.log(x) / x
        ans += y
    ans = (b - a) * ans / n
    return ans


def main():
    a = 1
    b = np.exp(1)
    n = 1000000
    print(monte_carlo_integration(a, b, n))


if __name__ == '__main__':
    main()
