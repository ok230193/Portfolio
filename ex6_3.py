import numpy as np


def lu_decomposition():
    E = np.array([[1, 1, 0, 3],
                  [2, 1, -1, 1],
                  [3, -1, -1, 2],
                  [-1, 2, 3, -1]])
    n = len(E)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        for k in range(i, n):
            sum = 0
            for j in range(i):
                sum += (L[i][j] * U[j][k])
            U[i][k] = E[i][k] - sum

        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                sum = 0
                for j in range(i):
                    sum += (L[k][j] * U[j][i])
                L[k][i] = (E[k][i] - sum) / U[i][i]

    return L, U


def main():
    L, U = lu_decomposition()

    print("L:")
    print(L)
    print("\nU:")
    print(U)


if __name__ == "__main__":
    main()
