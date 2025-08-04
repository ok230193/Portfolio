import numpy as np
import matplotlib.pyplot as plt


def cellular_automaton():
    rule_num = 110
    rule_list = np.empty(8)
    for i in range(8):
        rule_list[i] = rule_num >> i & 1

    cell = 101
    trial = 151

    np.random.seed(1)
    cells = np.random.randint(0, 2, (trial, cell))

    for trial in range(trial - 1):
        temp_cell = cells[trial, :]
        temp_cell = np.pad(temp_cell, 1)
        for i in range(1, cell + 1):
            test = 4 * temp_cell[i - 1] + 2 * temp_cell[i] + temp_cell[i + 1]
            cells[trial + 1, i - 1] = rule_list[test]

    return cells


def main():
    cells = cellular_automaton()
    plt.figure()
    plt.imshow(cells)
    plt.show()


if __name__ == '__main__':
    main()