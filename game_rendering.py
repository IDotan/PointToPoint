import pygame
import puzzle
from math import sqrt
from time import time
import webbrowser

WIDTH = 600
HEIGHT = 350
SCREEN_BG = (191, 191, 191)
CUBE_BG = (30, 30, 30)
CUBE_HIGHLIGHT = (51, 173, 255)
EMPTY_CUBE_SPACE = (115, 115, 115)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (160, 160, 160)
FPS = 30

pygame.init()


class Cube:
    def __init__(self, num, window, pos, size):
        """
        | class to store tile data
        :param num: cube number
        :param window: pygame.surface to render on
        :param pos: center position
        :param size: size of the cube
        """
        self.num = num
        self.parent_surface = window
        self.pos = pos
        self.size = size
        self.selected = False
        self.click_rad = None
        self.__cube_click_rad()

    def draw(self, solved=False):
        """
        | draw the cube on the board
        :param solved: bool, if the puzzle is solved
        """
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surface.fill(CUBE_BG)
        colors = board.get_tile_colors(self.num)
        circle_size = int(self.size*0.45)

        pygame.draw.circle(surface, colors[0], surface.get_rect().bottomleft, circle_size)
        pygame.draw.circle(surface, colors[1], surface.get_rect().topleft, circle_size)
        pygame.draw.circle(surface, colors[2], surface.get_rect().topright, circle_size)
        pygame.draw.circle(surface, colors[3], surface.get_rect().bottomright, circle_size)

        self.__draw_highlight(surface, solved, int(self.size * 0.15))
        surface = pygame.transform.rotate(surface, -45)
        self.parent_surface.blit(surface, surface.get_rect(center=self.pos))

    def __draw_highlight(self, surface, solved, size):
        """
        | draw cube boarder
        :param surface: cube's surface
        :param solved: bool, if the puzzle is solved
        :param size: boarder size width
        """
        if self.selected is True:
            pygame.draw.rect(surface, CUBE_HIGHLIGHT, surface.get_rect(), size)
        elif solved is False:
            pygame.draw.rect(surface, CUBE_BG, surface.get_rect(), size)

    def __cube_click_rad(self):
        """create detectable click radios for the cube"""
        x = self.pos[0] - int(self.size//2)
        y = self.pos[1] - int(self.size*0.3)
        self.click_rad = pygame.Rect((x, y, self.size, int(self.size*0.7)))


class PointGame:
    def __init__(self):
        """create and handle the puzzle GUI"""
        self.height = HEIGHT
        self.width = WIDTH
        self.window = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
        self.window.fill(SCREEN_BG)
        pygame.display.set_caption("Point To Point")
        pygame.display.set_allow_screensaver(True)
        board.random_board()  # start with a random board
        self.solved = False
        self.selected_cube = None
        self.dragging = None
        self.hint = False
        self.cubes = []
        self.rules_time = 0
        self.rules_stats = False
        self.cubes_pos = []
        self.cube_size = 0
        self.buttons = []
        self.__create_cubes()
        self.__create_buttons_data()
        self.clickable = []
        self.__create_clickable_data()

    def __check_buttons_clicked(self, pos):
        """
        | check if any button was clicked
        :param pos: mouse clicked position to check
        :return: True when a button was clicked
        """
        if pos[0] <= self.clickable[0][1][0] and pos[1] <= self.clickable[0][1][1]:
            if self.rules_stats:
                self.rules_time = 0
            else:
                self.rules_time = time() + 60
            return True
        if pos[0] <= self.clickable[1][1][0] and self.clickable[1][1][1] <= pos[1]:
            webbrowser.open('https://www.linkedin.com/in/idotan')
            return True
        for button in self.buttons:
            if button[1][0] <= pos[0] <= button[1][0] + button[1][2] \
                    and button[1][1] <= pos[1] <= button[1][1] + button[1][3]:
                if button[0] == 'Shuffle':
                    if self.rules_stats is False:
                        if self.selected_cube:
                            self.selected_cube.selected = False
                        self.solved = False
                        board.random_board()
                    return True
                elif button[0] == 'Hint':
                    self.hint = False if self.hint else True
                    return True

    def __blit_text(self, text, width, x, y, font, center=False, color=TEXT_COLOR):
        """
        | blit given text on the screen
        :param text: text to show
        :param width: max width available for the text
        :param x: top left x of text available space
        :param y: top left y of text available space
        :param font: pygame.font object
        :param center: bool, True to center text
        :param color: text color
        """
        def fit_lines(sub_line):
            """
            | sub function to split text to mach available space
            :param sub_line: str, text to fit in the space
            :return: list of fitted text
            """
            if sub_line == '\n':
                return sub_line
            words = sub_line.split()
            sub_line = []
            while len(words) > 0:
                line_words = []
                while len(words) > 0:
                    line_words.append(words.pop(0))
                    f_w, f_h = font.size(' '.join(line_words + words[:1]))
                    if f_w > width:
                        break
                temp_line = ' '.join(line_words)
                sub_line.append(temp_line)
            return sub_line

        lines = []
        if type(text) is list:
            for line in text:
                split_lines = fit_lines(line)
                for parts in split_lines:
                    lines.append(parts)
        else:
            lines = fit_lines(text)

        y_offset = 0
        x_center = x + int(width // 2)
        for line in lines:
            fw, fh = font.size(line)
            if line == '\n':
                y_offset += fh
                continue
            tx = x_center - int(fw // 2) if center else x
            ty = y + y_offset
            font_surface = font.render(line, True, color)
            self.window.blit(font_surface, (tx, ty))
            y_offset += fh

    def __show_rules(self):
        """render the puzzle rules"""
        text = ['Rotate and move the tiles so every  tile\'s corner will touch the same color as it self.',
                '\n',
                'Adjust the tiles using drag and drop, rotate with mousewheel or keyboard left and right.']
        width = int(self.width * 0.7)
        x = int(self.height * 0.01)
        y = int(self.width * 0.07)
        font = pygame.font.Font(None, int(self.height * 0.12))
        self.__blit_text(text, width, x, y, font)

    def __rules(self):
        """render rules button"""
        if self.rules_stats:
            text = 'Back'
        else:
            text = 'Click to show rules'
        width = self.width - 5
        x = int(self.height * 0.01)
        y = int(self.width * 0.01)
        font = pygame.font.Font(None, int(self.height * 0.08))
        fw, fh = font.size(text)
        self.clickable[0][1][0], self.clickable[0][1][1] = fw + x, fh
        self.__blit_text(text, width, x, y, font)

    def __credit(self):
        """render credit watermark"""
        text = ['Created by:', 'linkedin.com/in/IDotan']
        font = pygame.font.Font(None, int(self.height * 0.06))
        width, _ = font.size(text[1])
        fw, fh = font.size(text[1])
        x = int(self.width * 0.01)
        self.clickable[1][1][0] = fw + x
        self.clickable[1][1][1] = self.height - fh * 2
        y = self.clickable[1][1][1] - self.height * 0.01
        self.__blit_text(text, width, x, y, font, color=(0, 122, 204))

    def __blit_hint(self):
        """render hint"""
        text = ['Hint:', 'The center 4 must be either red or yellow']
        width = self.buttons[0][1][2]
        x = self.buttons[0][1][0]
        y = self.buttons[1][1][1] + int(self.height * 0.2)
        font = pygame.font.Font(None, int(width * 0.2))
        self.__blit_text(text, width, x, y, font, True)

    def __create_clickable_data(self):
        """create clickable data blueprint"""
        self.clickable = [['Rules', [0, 0]],
                          ['Credit', [0, 0]]]

    def __create_buttons_data(self):
        """create button data"""
        x_gap = self.width - int(self.width * 0.02)
        y_gap = int(self.height * 0.025)
        y_top_gap = int(self.height * 0.15)
        button_width = int(self.width * 0.25)
        button_height = int(self.height * 0.15)
        self.buttons = [['Shuffle', (x_gap - button_width, y_top_gap, button_width, button_height)],
                        ['Hint', (x_gap - button_width, y_top_gap + button_height + y_gap,
                                  button_width, button_height)]]

    def __draw_buttons(self):
        """draw buttons in self.buttons"""
        for data in self.buttons:
            button = pygame.draw.rect(self.window, BUTTON_COLOR, data[1], border_radius=20)
            fnt = pygame.font.SysFont("cambria", int(data[1][3] * 0.5))
            text = fnt.render(data[0], True, TEXT_COLOR)
            self.window.blit(text, (button.center[0] - text.get_width() / 2,
                                    button.center[1] - text.get_height() / 2))

    def __resize(self, width, height):
        """resize the screen and all needed data"""
        if height != self.height and width == self.width:
            width = int(height * 1.7)
        elif width != self.width and height == self.height:
            height = int(width / 1.7)
        else:
            height = int(width / 1.7)

        self.width = width
        self.height = height
        self.window = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
        self.cubes = []
        self.__create_cubes()
        self.__create_buttons_data()
        self.__create_clickable_data()

    def __draw_empty_space(self):
        """draw empty tile space"""
        surface = pygame.Surface((self.cube_size, self.cube_size), pygame.SRCALPHA)
        surface.fill(EMPTY_CUBE_SPACE)
        surface = pygame.transform.rotate(surface, -45)
        self.window.blit(surface, surface.get_rect(center=self.cubes_pos[self.dragging.num]))

    def __create_cubes(self):
        """create puzzle tiles data"""
        self.cube_size = int(self.width * 0.7 // 3 * 0.65)
        cube_gaps = int(self.width*0.02)
        cube_rotated_space = int(sqrt((self.cube_size**2)*2))
        x_offset = int(self.width * 0.02)
        y_offset = int(self.height * 0.3)
        mid_row_y = y_offset + cube_rotated_space//2 + cube_gaps//2
        bottom_row_y = y_offset + cube_rotated_space + cube_gaps
        trios_x = [x_offset + cube_rotated_space/2,
                   x_offset + cube_gaps + cube_rotated_space + cube_rotated_space / 2,
                   x_offset + cube_gaps * 2 + cube_rotated_space * 2 + cube_rotated_space / 2]
        self.cubes_pos = [
            # top
            (trios_x[0], y_offset), (trios_x[1], y_offset), (trios_x[2], y_offset),
            # mid
            (x_offset + cube_rotated_space + cube_gaps//2, mid_row_y),
            (x_offset + cube_rotated_space * 2 + cube_gaps//2 + cube_gaps, mid_row_y),
            # bottom
            (trios_x[0], bottom_row_y), (trios_x[1], bottom_row_y), (trios_x[2], bottom_row_y),
        ]
        for i in range(8):
            self.cubes.append(Cube(i, self.window, self.cubes_pos[i], self.cube_size))

    def __mouse_down(self, pos):
        """action to take when mouse left button down"""
        cube_clicked = False
        if not self.__check_buttons_clicked(pos):
            if self.solved is False and self.rules_stats is False:
                for cube in self.cubes:
                    if cube.click_rad.collidepoint(pos):
                        cube_clicked = True
                        if self.selected_cube:
                            self.selected_cube.selected = False
                        cube.selected = True
                        self.selected_cube = cube
                        self.dragging = cube
                        break
                if cube_clicked is False and self.selected_cube:
                    self.selected_cube.selected = False
                    self.selected_cube = False

    def __mouse_up(self, pos):
        """action to take when mouse left button up"""
        if self.dragging:
            self.dragging.pos = self.cubes_pos[self.dragging.num]
        for cube in self.cubes:
            if cube.click_rad.collidepoint(pos):
                if self.dragging:
                    if cube.num != self.dragging.num:
                        board.switch_tiles(cube.num, self.dragging.num)
                        cube.selected = True
                        self.selected_cube = cube
                        self.dragging.selected = False
                        break
                    elif cube.num == self.dragging.num:
                        break
        self.dragging = None

    def __mouse_over_clickable(self, pos):
        """action to take when mouse hovering over clickable"""
        cursor = pygame.SYSTEM_CURSOR_ARROW
        found = False
        if self.dragging is None:
            if pos[0] <= self.clickable[0][1][0] and pos[1] <= self.clickable[0][1][1]:
                cursor = pygame.SYSTEM_CURSOR_HAND
                found = True
            elif pos[0] <= self.clickable[1][1][0] and self.clickable[1][1][1] <= pos[1]:
                cursor = pygame.SYSTEM_CURSOR_HAND
                found = True
            if found is False:
                for button in self.buttons:
                    if button[1][0] <= pos[0] <= button[1][0] + button[1][2] \
                            and button[1][1] <= pos[1] <= button[1][1] + button[1][3]:
                        cursor = pygame.SYSTEM_CURSOR_HAND
        pygame.mouse.set_cursor(cursor)

    def __end_loop_renders(self):
        """check if puzzle solved and endloop renders"""
        if self.solved is False:
            self.solved = board.check_board()
        if self.solved and self.selected_cube:
            self.selected_cube.selected = False
        self.window.fill(SCREEN_BG)
        self.__draw_buttons()
        self.__credit()
        self.__rules()
        if self.hint:
            self.__blit_hint()
        if self.rules_stats:
            self.__show_rules()
        else:
            for cube in self.cubes:
                cube.draw(self.solved)
            if self.dragging:
                self.__draw_empty_space()
                self.dragging.draw()
        pygame.display.flip()

    def __mainloop(self):
        """puzzle mainloop"""
        clock = pygame.time.Clock()
        run = True
        while run:
            self.rules_stats = self.rules_time > time()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.__mouse_over_clickable(pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.VIDEORESIZE:
                    self.__resize(event.w, event.h)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouse_down(pygame.mouse.get_pos())

                elif self.solved is False and self.rules_stats is False:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.__mouse_up(pygame.mouse.get_pos())

                    elif self.dragging and event.type == pygame.MOUSEMOTION:
                        self.dragging.pos = pygame.mouse.get_pos()

                    elif event.type == pygame.KEYDOWN:
                        key = event.key
                        if self.selected_cube:
                            if key == 1073741903:  # right
                                board.spin_tile(self.selected_cube.num, 1)
                            elif key == 1073741904:  # left
                                board.spin_tile(self.selected_cube.num, -1)

                    elif event.type == pygame.MOUSEWHEEL:
                        direction = event.y
                        if self.selected_cube:
                            if direction == -1:  # right
                                board.spin_tile(self.selected_cube.num, 1)
                            elif direction == 1:  # left
                                board.spin_tile(self.selected_cube.num, -1)

            self.__end_loop_renders()
            clock.tick(30)

    def __call__(self, *args, **kwargs):
        """start the game loop"""
        self.__mainloop()


board = puzzle.PuzzleTiles()
game = PointGame()
game()
