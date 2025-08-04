import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def life_game():
    loop_num = 300
    output = np.zeros((loop_num, 50, 50), dtype="int")

    np.random.seed(1)
    cells = np.random.randint(0, 2, (50, 50))
    cells = np.pad(cells, (1, 1))

    for t in range(loop_num):
        new_cells = np.zeros(cells.shape, dtype="int")
        for y in range(1, 51):
            for x in range(1, 51):
                part_sum = np.sum(cells[y - 1:y + 2, x - 1:x + 2]) - cells[y, x]

                if cells[y, x] == 1:
                    if part_sum == 2 or part_sum == 3:
                        new_cells[y, x] = 1
                    elif part_sum <= 1:
                        new_cells[y, x] = 0
                    elif part_sum >= 4:
                        new_cells[y, x] = 0
                elif cells[y, x] == 0:
                    if part_sum == 3:
                        new_cells[y, x] = 1
        cells = new_cells
        output[t] = new_cells[1:51, 1:51]

    return output


def main():
    output = life_game()
    frames = []
    fig = plt.figure()
    for cells in output:
        frames.append([plt.imshow(cells)])

    ani = animation.ArtistAnimation(fig, frames, interval=100)
    plt.show()


if __name__ == '__main__':
    main()
