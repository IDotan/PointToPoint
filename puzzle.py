from random import randint, shuffle

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class PuzzleTiles:
    def __init__(self):
        # tile in tiles index:
        # tile[0] - rotation, tile[1-4] - tile color order
        self.tiles = [[0, YELLOW, BLUE, RED, GREEN],
                      [0, RED, BLUE, GREEN, YELLOW],
                      [0, GREEN, RED, YELLOW, BLUE],
                      [0, GREEN, RED, YELLOW, BLUE],
                      [0, YELLOW, GREEN, BLUE, RED],
                      [0, YELLOW, GREEN, BLUE, RED],
                      [0, BLUE, YELLOW, RED, GREEN],
                      [0, RED, BLUE, YELLOW, GREEN]]
        self.trios = []

    def get_tile_colors(self, tile):
        """
        | return the color show order
        :param tile: tile index
        :return: list, colors order to render
        """
        pos = self.tiles[tile][0]
        if pos == 1:
            return [self.tiles[tile][4], self.tiles[tile][1], self.tiles[tile][2], self.tiles[tile][3]]
        if pos == 2:
            return [self.tiles[tile][3], self.tiles[tile][4], self.tiles[tile][1], self.tiles[tile][2]]
        if pos == 3:
            return [self.tiles[tile][2], self.tiles[tile][3], self.tiles[tile][4], self.tiles[tile][1]]
        return [self.tiles[tile][1], self.tiles[tile][2], self.tiles[tile][3], self.tiles[tile][4]]

    def spin_tile(self, tile, direction):
        """
        | spin game tile right or left
        :param tile: tile index number
        :param direction: 1 - right, (-1) - left
        """
        self.tiles[tile][0] += direction
        if self.tiles[tile][0] == 4:
            self.tiles[tile][0] = 0
        elif self.tiles[tile][0] == -1:
            self.tiles[tile][0] = 3

    def random_board(self):
        """
        | create a random puzzle board
        """
        for tile in self.tiles:
            tile[0] = randint(0, 3)
        shuffle(self.tiles)

    def switch_tiles(self, first, second):
        """
        | switch position of 2 tiles
        :param first: tile index to switch
        :param second: tile index to switch
        """
        this = self.tiles[first]
        other = self.tiles[second]
        self.tiles[first] = other
        self.tiles[second] = this

    def __get_all_trios(self, current_color_pos):
        """
        | fill self.trios with the current colors
        | trio will be the color when complete, false otherwise
        :param current_color_pos: list of tiles color
        """
        self.trios = [
            current_color_pos[7][0] if current_color_pos[6][2] == current_color_pos[4][3] ==
            current_color_pos[7][0] else False,
            current_color_pos[6][0] if current_color_pos[5][2] == current_color_pos[3][3] ==
            current_color_pos[6][0] else False,
            current_color_pos[5][1] if current_color_pos[5][1] == current_color_pos[3][0] ==
            current_color_pos[0][3] else False,
            current_color_pos[0][2] if current_color_pos[0][2] == current_color_pos[3][1] ==
            current_color_pos[1][0] else False,
            current_color_pos[1][2] if current_color_pos[1][2] == current_color_pos[4][1] ==
            current_color_pos[2][0] else False,
            current_color_pos[2][3] if current_color_pos[2][3] == current_color_pos[4][2] ==
            current_color_pos[7][1] else False
        ]

    def check_board(self):
        """
        | check if the board is solved
        :return: True when solved
        """
        current_color_pos = []
        for i in range(8):
            current_color_pos.append(self.get_tile_colors(i))

        center = current_color_pos[1][3] if current_color_pos[1][3] == current_color_pos[3][2] == \
            current_color_pos[4][0] == current_color_pos[6][1] else False
        if center is False:
            return False

        self.__get_all_trios(current_color_pos)
        for trio in self.trios:
            if trio is False:
                return False

        # second main color across
        if (self.trios[0] != self.trios[3] and self.trios[3] == center) or \
                (self.trios[1] != self.trios[4] and self.trios[1] == center):
            return False

        return True
