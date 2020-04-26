from board import Board, get_arounds, calc_pos
import math


class Search:
    _RANGE = 8

    def __init__(self):
        self.conditions = []
        self.cells_table = {}
        self.mines_num = 0
        self.board_width = 0
        self.board_height = 0
        self.is_final = False

    def search(self, board: Board):
        self.__init__()
        self.board_width = board.board.shape[1]
        self.board_height = board.board.shape[0]
        self.mines_num = board.mines_num
        self._search_range(board, 0)
        count = 0
        uncover_cells = set()
        flag_cells = set()
        while not self.is_final:
            self.is_final = True
            self.conditions = []
            self.cells_table = {}
            uncover, flag = self._search_range(board, count)
            uncover_cells |= uncover
            flag_cells |= flag
            count += 1
        for cell in uncover_cells:
            x, y = cell
            board.uncover(x, y)
        for cell in flag_cells:
            x, y = cell
            board.flag(x, y)
        return uncover_cells or flag_cells

    def _search_range(self, board: Board, start):
        neighboring_cells = set()
        place_conditions = []
        skip = start

        for y in range(self.board_height):
            for x in range(self.board_width):
                if board.board[y, x] < 1:
                    continue
                arounds = get_arounds(board.board, x, y, self.board_width, self.board_height)
                covered_cells = list(filter(lambda kv: kv[1] == Board.COVERED, arounds.items()))
                if not covered_cells:
                    continue
                if skip:
                    skip -= 1
                    continue
                covered_cells_pos = list(map(lambda kv: calc_pos(kv[0], x, y), covered_cells))
                if len(neighboring_cells.union(set(covered_cells_pos))) > self._RANGE:
                    self.is_final = False
                    break
                neighboring_cells |= set(covered_cells_pos)
                around_mines_num = board.board[y, x] - tuple(arounds.values()).count(Board.FLAGGED)
                place_conditions.append((around_mines_num, covered_cells_pos))
        ordered_cells = tuple(neighboring_cells)
        ordered_cells_key_dic = {k: v for v, k in enumerate(ordered_cells)}

        for place_cond in place_conditions:
            cond_cells = tuple(map(lambda place: ordered_cells_key_dic[place], place_cond[1]))
            self.conditions.append((place_cond[0], cond_cells))

        self._put_mine((False,) * len(ordered_cells))
        probable_cells_list = [k for k, v in self.cells_table.items() if v]
        probability_list = [0] * len(ordered_cells)
        for cells in probable_cells_list:
            probability_list = [p + int(c) for p, c in zip(probability_list, cells)]
        if not len(probable_cells_list):
            return set(), set()
        probability_list = [p / len(probable_cells_list) for p in probability_list]
        uncover_cells = set()
        flag_cells = set()
        for index, value in enumerate(probability_list):
            if math.isclose(value, 0, abs_tol=1e-10):
                uncover_cells.add(ordered_cells[index])
            if math.isclose(value, 1, abs_tol=1e-10):
                flag_cells.add(ordered_cells[index])
        return uncover_cells, flag_cells

    def _put_mine(self, cells):
        if cells in self.cells_table:
            return
        if cells.count(True) > self.mines_num:
            self.cells_table[cells] = False
            return

        self.cells_table[cells] = not any(
            map(lambda cond: not self._verify_around_mines_num(cells, cond), self.conditions))
        for index, value in enumerate(cells):
            if value:
                continue
            mine_added_cells = list(cells[:])
            mine_added_cells[index] = True
            self._put_mine(tuple(mine_added_cells))

    @staticmethod
    def _verify_around_mines_num(cells, cond):
        around_mines_num = cond[0]
        cond_cells = cond[1]
        num = tuple(map(lambda x: cells[x], cond_cells)).count(True)
        return around_mines_num == num
