from typing import List, Iterable, Tuple

def visibilities(grid: List[List[int]]) -> Iterable[Tuple[int]]:
    pass


if __name__ == '__main__':
    def checker(func, grid):
        result = func([row[:] for row in grid])
        BLACK, MOVES = -1, ((-1, 0), (1, 0), (0, -1), (0, 1))
        in_grid = lambda i, j: 0 <= i < len(grid) and 0 <= j < len(grid[0])
        for item in result:
            if not (isinstance(item, (tuple, list)) and len(item) == 2 and
                    all(isinstance(n, int) for n in item)):
                print(f"You should give tuples/lists of 2 ints, not {item}.")
                return False
            i, j = item
            if not in_grid(i, j):
                print(f"{(i, j)} is outside the grid.")
                return False
            if grid[i][j] > 0:
                print("You can't put a black box on the "
                      f"number {grid[i][j]} at {(i, j)}.")
                return False
            if grid[i][j] == BLACK:
                print(f"You can't put a black box twice at {(i, j)}.")
                return False
            for x, y in ((i + di, j + dj) for di, dj in MOVES):
                if in_grid(x, y) and grid[x][y] == BLACK: # RULE 1
                    print(f"You can't put a black box at {(x, y)} because "
                          f"there is a box at {(i, j)}, it's too close.")
                    return False
            grid[i][j] = BLACK
        from numpy import array
        from scipy.ndimage import label # Powerful tool.
        bool_array = array([[n != BLACK for n in row] for row in grid])
        num_pieces = label(bool_array)[1]
        if num_pieces > 1: # RULE 2
            print("White boxes in the grid should not be separated "
                  f"into {num_pieces} pieces by black boxes.")
            return False
        numbers = ((i, j, n) for i, row in enumerate(grid)
                             for j, n in enumerate(row) if n > 0)
        for i, j, n in numbers:
            visibility_from_n = 1
            for di, dj in MOVES:
                x, y = i + di, j + dj
                while in_grid(x, y) and grid[x][y] != BLACK:
                    visibility_from_n += 1
                    x, y = x + di, y + dj
            if visibility_from_n != n: # RULE 3
                print(f"The box at {(i, j)} should see "
                      f"{n} boxes, not {visibility_from_n}.")
                return False
        return True

    GRIDS = (('5x5', [[0, 0, 4, 0, 6],
                      [0, 6, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 5, 0],
                      [6, 0, 7, 0, 0]]),

             ('5x8', [[0, 0, 0, 0, 0, 0, 4, 7],
                      [0, 0, 0, 0, 4, 0, 3, 0],
                      [0, 0, 8, 0, 0, 7, 0, 0],
                      [0, 4, 0, 6, 0, 0, 0, 0],
                      [6, 5, 0, 0, 0, 0, 0, 0]]),

             ('6x9', [[6, 0, 0, 8, 0, 0, 4, 0, 0],
                      [0, 0, 0, 9, 0, 0, 0, 0, 0],
                      [7, 3, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 8],
                      [0, 0, 0, 0, 0, 2, 0, 0, 0],
                      [0, 0, 9, 0, 0, 8, 0, 0, 12]]),

             ('8x12', [[0, 0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 0],
                       [0, 5, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                       [0, 6, 0, 0, 0, 13, 0, 0, 0, 10, 0, 0],
                       [0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 8, 6],
                       [8, 3, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
                       [0, 0, 9, 0, 0, 0, 5, 0, 0, 0, 7, 0],
                       [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 10, 0],
                       [0, 0, 0, 0, 0, 13, 0, 0, 7, 0, 0, 0]]))

    for dim, grid in GRIDS:
        assert checker(visibilities, grid), f"You failed on the grid {dim}."

