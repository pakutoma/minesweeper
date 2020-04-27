from board import Board, get_arounds, calc_pos
import numpy as np
from search import Search
import time

def solver(board):
    width = board.board.shape[1]
    height = board.board.shape[0]
    count = 0
    for y in range(height):
        for x in range(width):
            if board.board[y, x] < 1:
                continue
            arounds = get_arounds(board.board, x, y, width, height)
            # if len(list(filter(lambda k, v: v == Board.COVERED, arounds.items()))) == 0:
            #     continue
            mine_num = board.board[y, x]
            covered_num = list(arounds.values()).count(Board.COVERED)
            flagged_num = list(arounds.values()).count(Board.FLAGGED)
            if flagged_num == mine_num and covered_num > 0:
                for pos, value in arounds.items():
                    if value == Board.COVERED:
                        cell_x, cell_y = calc_pos(pos, x, y)
                        board.uncover(cell_x, cell_y)
                        count += 1
            if covered_num + flagged_num == mine_num and covered_num > 0:
                for pos, value in arounds.items():
                    if value == Board.COVERED:
                        cell_x, cell_y = calc_pos(pos, x, y)
                        board.flag(cell_x, cell_y)
                        count += 1
    if count == 0:
        return False
        # c, r = np.where(board.board == Board.COVERED)
        # print('random')
        # board.uncover(r[0], c[0])
    else:
        return True


if __name__ == '__main__':
    board = Board()
    board.init()
    time.sleep(0.5)
    board.load()
    search = Search()
    for i in range(100):
        if not search.search(board) and not solver(board):
            break
        board.load()
