import numpy as np


def gaussian_elimination():
    A = np.array([
        [4, -1, 0, -1, 0, 0, 0, 0, 0],
        [-1, 4, -1, 0, -1, 0, 0, 0, 0],
        [0, -1, 4, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, 4, -1, 0, -1, 0, 0],
        [0, -1, 0, -1, 4, -1, 0, -1, 0],
        [0, 0, -1, 0, -1, 4, 0, 0, -1],
        [0, 0, 0, -1, 0, 0, 4, -1, 0],
        [0, 0, 0, 0, -1, 0, -1, 4, -1],
        [0, 0, 0, 0, 0, -1, 0, -1, 4]], dtype='float')
    B = np.array([[0, 0, 0.25, 0, 0, 0.5, 0.25, 0.5, 1.5]]).T
    X = np.empty((9, 1))
    E = np.concatenate([A, B], 1)

    for i in range(8):
        E[i, :] = E[i, :]/E[i, i]
        E[i+1:, :] = E[i+1:, :] - E[i+1:, i:i+1] @ E[i:i+1, :]
    E[8, :] = E[8, :] / E[8, 8]

    A = E[:, 0:-1]
    B = E[:, -1:]

    X[8] = B[8]
    for i in range(7, -1, -1):
        X[i] = B[i] - A[i:i+1, i+1:] @ X[i+1:]

    return X


def main():
    print(gaussian_elimination())


if __name__ == '__main__':
    main()