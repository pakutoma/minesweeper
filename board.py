import pyautogui
import time
import numpy as np
from PIL import Image

class Board:
    COVERED = -1
    FLAGGED = -2
    _SQUARE_WH = 25
    _SQUARE_LINE_WIDTH = 2
    _BOARD_WIDTH = 600
    _BOARD_HEIGHT = 500
    _TEMPLATE_WH = 21
    _TEMPLATE_THRESHOLD = 1
    _ALL_MINES_NUM = 99

    def __init__(self):
        self._board_x = 0
        self._board_y = 0
        self._board_width = 0
        self._board_height = 0
        self.board = np.full((self._BOARD_HEIGHT // self._SQUARE_WH, self._BOARD_WIDTH // self._SQUARE_WH), Board.COVERED)
        self.mines_num = self._ALL_MINES_NUM

    def _init_template(self):
        self._templates = []
        for i in range(8):
            self._templates.append([])
            try:
                w_img = Image.open('images/' + str(i) + 'w.png').convert('RGB')
                self._templates[i].append(np.array(w_img))
            except FileNotFoundError:
                pass
            try:
                b_img = Image.open('images/' + str(i) + 'b.png').convert('RGB')
                self._templates[i].append(np.array(b_img))
            except FileNotFoundError:
                pass
        failed_img = Image.open('images/failed.png').convert('RGB')
        self._template_failed = np.array(failed_img)

    def init(self):
        self._init_template()
        self._board_x, self._board_y, self._board_width, self._board_height = pyautogui.locateOnScreen(
            'images/board.png')
        pyautogui.moveTo(self._board_x + self._SQUARE_WH // 2, self._board_y + self._SQUARE_WH // 2)
        pyautogui.click()
        self.mines_num = self._ALL_MINES_NUM

    def load(self):
        pyautogui.moveTo(self._board_x + self._SQUARE_WH // 2, self._board_y + self._SQUARE_WH // 2)
        time.sleep(0.5)
        pil_img = pyautogui.screenshot("test.png",
                                       region=(self._board_x, self._board_y, self._board_width, self._board_height))
        board_img = np.array(pil_img)
        if self._search_square(board_img, self._template_failed):
            raise RuntimeError("sweep failed.")
        for template_num, template_colors in enumerate(self._templates):
            places = []
            for index, template in enumerate(template_colors):
                if template is None:
                    continue
                places += self._search_square(board_img, template)
            for x, y in places:
                self.board[y, x] = template_num
        print(self.board)

    def uncover(self, x, y):
        pyautogui.moveTo(self._board_x + x * self._SQUARE_WH + self._SQUARE_WH // 2,
                         self._board_y + y * self._SQUARE_WH + self._SQUARE_WH // 2)
        pyautogui.click()
        self.board[y, x] = 8
        print('uncover', x, y)

    def flag(self, x, y):
        pyautogui.moveTo(self._board_x + x * self._SQUARE_WH + self._SQUARE_WH // 2,
                         self._board_y + y * self._SQUARE_WH + self._SQUARE_WH // 2)
        pyautogui.rightClick()
        self.board[y, x] = -2
        self.mines_num -= 1
        print('flag', x, y)

    def _search_square(self, board_img, template):
        places = []
        for y in range(0, self._BOARD_HEIGHT, self._SQUARE_WH):
            top = y + self._SQUARE_LINE_WIDTH
            bottom = y + self._SQUARE_WH - self._SQUARE_LINE_WIDTH
            for x in range(0, self._BOARD_WIDTH, self._SQUARE_WH):
                left = x + self._SQUARE_LINE_WIDTH
                right = x + self._SQUARE_WH - self._SQUARE_LINE_WIDTH
                square = board_img[top:bottom, left:right]
                if np.array_equal(square, template):
                    places.append((x // self._SQUARE_WH, y // self._SQUARE_WH))
        return places


def get_arounds(board, x, y, width, height):
    arounds = {}
    if x > 0 and y > 0:
        arounds[0] = board[y - 1, x - 1]
    if y > 0:
        arounds[1] = board[y - 1, x]
    if x < width - 1 and y > 0:
        arounds[2] = board[y - 1, x + 1]
    if x > 0:
        arounds[3] = board[y, x - 1]
    if x < width - 1:
        arounds[4] = board[y, x + 1]
    if x > 0 and y < height - 1:
        arounds[5] = board[y + 1, x - 1]
    if y < height - 1:
        arounds[6] = board[y + 1, x]
    if x < width - 1 and y < height - 1:
        arounds[7] = board[y + 1, x + 1]
    return arounds


def calc_pos(pos, x, y):
    if pos in [0, 3, 5]:
        cell_x = x - 1
    elif pos in [1, 6]:
        cell_x = x
    else:
        cell_x = x + 1
    if pos < 3:
        cell_y = y - 1
    elif pos < 5:
        cell_y = y
    else:
        cell_y = y + 1
    return cell_x, cell_y