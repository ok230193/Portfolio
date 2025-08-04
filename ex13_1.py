import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def traffic_simulation():
    cell_size = 100
    cell = np.zeros((100, cell_size), dtype='int')
    cell[0, 20:60] = 1

    rule_num = 184
    rule_list = np.empty(8)

    for i in range(8):
        rule_list[i] = rule_num >> i & 1

    for i in range(1, 100):
        temp_cells = np.pad(cell[i - 1], 1)
        for j in range(1, cell_size + 1):
            num = 4 * temp_cells[j - 1] + 2 * temp_cells[j] + temp_cells[j + 1]
            cell[i, j - 1] = rule_list[num]
        if i % 2 == 0:
            cell[i, 0] = 1

    return cell


def main():
    output = traffic_simulation()
    frames = []
    fig = plt.figure()
    for cells in output:
        frames.append([plt.imshow(cells.reshape(1, -1))])

    ani = animation.ArtistAnimation(fig, frames, interval=100)
    plt.show()


if __name__ == '__main__':
    main()
