import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def langtons_ant():
    ants = [Ant(45, 50), Ant(50, 55), Ant(55, 50)]
    loop_num = 7000
    cell_size = 100
    cell = np.zeros((cell_size, cell_size), dtype='int')
    output = np.zeros((loop_num, cell_size, cell_size), dtype='int')
    output[0] = cell

    for i in range(1, loop_num):
        for ant in ants:
            cell[ant.get_pos()] = ant.check_cell(cell[ant.get_pos()])
            ant.forward(cell_size)
        output[i] = cell

    return output


class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction_list = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self.direction_num = 0

    def check_cell(self, cell_color):
        if cell_color == 0:
            self.direction_num = (self.direction_num + 1) % 4
            return 1
        elif cell_color == 1:
            self.direction_num = (self.direction_num - 1) % 4
            return 0

    def get_pos(self):
        return self.y, self.x

    def forward(self, cell_size):
        next_pos = self.direction_list[self.direction_num]
        self.x = (self.x + next_pos[0]) % cell_size
        self.y = (self.y + next_pos[1]) % cell_size


def main():
    output = langtons_ant()
    fig, ax = plt.subplots()
    frames = [[ax.imshow(output[0])]]
    for i in range(1, 7000):
        im = ax.imshow(output[i], animated=True)
        frames.append([im])
    ani = animation.ArtistAnimation(fig, frames, interval=10, blit=True)
    plt.show()


if __name__ == '__main__':
    main()
