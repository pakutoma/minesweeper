from board import Board
import numpy as np


def _get_arounds(board, x, y, width, height):
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


def _calc_pos(pos, x, y):
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


def solver(board):
    width = board.board.shape[1]
    height = board.board.shape[0]
    count = 0
    for x in range(width):
        for y in range(height):
            if board.board[y, x] < 1:
                continue
            arounds = _get_arounds(board.board, x, y, width, height)
            mine_num = board.board[y, x]
            covered_num = list(arounds.values()).count(Board.COVERED)
            flagged_num = list(arounds.values()).count(Board.FLAGGED)
            if flagged_num == mine_num and covered_num > 0:
                for pos, value in arounds.items():
                    if value == Board.COVERED:
                        cell_x, cell_y = _calc_pos(pos, x, y)
                        board.uncover(cell_x, cell_y)
                        count += 1
            if covered_num + flagged_num == mine_num and covered_num > 0:
                for pos, value in arounds.items():
                    if value == Board.COVERED:
                        cell_x, cell_y = _calc_pos(pos, x, y)
                        board.flag(cell_x, cell_y)
                        count += 1
    if count == 0:
        c, r = np.where(board.board == -1)
        print('random')
        board.uncover(r[0], c[0])


if __name__ == '__main__':
    board = Board()
    board.init()
    board.load()
    for i in range(100):
        solver(board)
        board.load()
