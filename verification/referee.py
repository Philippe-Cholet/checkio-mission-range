"""
CheckiOReferee is a base referee for checking you code.
    arguments:
        tests -- the dict contains tests in the specific structure.
            You can find an example in tests.py.
        cover_code -- is a wrapper for the user function and additional operations before give data
            in the user function. You can use some predefined codes from checkio.referee.cover_codes
        checker -- is replacement for the default checking of an user function result. If given, then
            instead simple "==" will be using the checker function which return tuple with result
            (false or true) and some additional info (some message).
            You can use some predefined codes from checkio.referee.checkers
        add_allowed_modules -- additional module which will be allowed for your task.
        add_close_builtins -- some closed builtin words, as example, if you want, you can close "eval"
        remove_allowed_modules -- close standard library modules, as example "math"
checkio.referee.checkers
    checkers.float_comparison -- Checking function fabric for check result with float numbers.
        Syntax: checkers.float_comparison(digits) -- where "digits" is a quantity of significant
            digits after coma.
checkio.referee.cover_codes
    cover_codes.unwrap_args -- Your "input" from test can be given as a list. if you want unwrap this
        before user function calling, then using this function. For example: if your test's input
        is [2, 2] and you use this cover_code, then user function will be called as checkio(2, 2)
    cover_codes.unwrap_kwargs -- the same as unwrap_kwargs, but unwrap dict.
"""

from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee
# from checkio.referees import cover_codes
# from checkio.referees import checkers

from tests import TESTS

from numpy import array
from scipy.ndimage import label

BLACK, MOVES = -1, ((-1, 0), (1, 0), (0, -1), (0, 1))

def checker(grid, result):
    in_grid = lambda i, j: 0 <= i < len(grid) and 0 <= j < len(grid[0])
    for item in result:
        if not (isinstance(item, (tuple, list)) and len(item) == 2 and
                all(isinstance(n, int) for n in item)):
            return False, ("You should give tuples/lists of 2 ints, "
                           f"not {item}.", "Invalid")
        i, j = item
        if not in_grid(i, j):
            return False, (f"{(i, j)} is outside the grid.", "Invalid")
        if grid[i][j] > 0:
            return False, ("You can't put a black box on the "
                           f"number {grid[i][j]} at {(i, j)}.",
                           "Valid", 0, ((i, j),))
        if grid[i][j] == BLACK:
            return False, (f"You can't put a black box twice at {(i, j)}.",
                            "Valid", 0, ((i, j),))
        for x, y in ((i + di, j + dj) for di, dj in MOVES):
            if in_grid(x, y) and grid[x][y] == BLACK: # RULE 1
                return False, (f"You can't put a black box at {(x, y)} "
                               f"because there is a box at {(i, j)}, "
                               "it's too close.",
                               "Valid", 1, ((x, y),))
        grid[i][j] = BLACK
    bool_array = array([[n != BLACK for n in row] for row in grid])
    labeled_grid, num_pieces = label(bool_array)
    if num_pieces > 1: # RULE 2
        return False, ("White boxes in the grid should not be separated "
                       f"into {num_pieces} pieces by black boxes.",
                       "Valid", 2, labeled_grid.tolist())
    numbers = ((i, j, n) for i, row in enumerate(grid)
                         for j, n in enumerate(row) if n > 0)
    for i, j, n in numbers:
        visibility_from_n = 1
        ends = []
        for di, dj in MOVES:
            x, y = i + di, j + dj
            while in_grid(x, y) and grid[x][y] != BLACK:
                visibility_from_n += 1
                x, y = x + di, y + dj
            ends.append((x, y))

        if visibility_from_n != n: # RULE 3
            return False, (f"The box at {(i, j)} should see "
                           f"{n} boxes, not {visibility_from_n}.",
                           "Valid", 3, ends)
    return True, ("Great!", "Valid")


cover_iterable = '''
def cover(func, data):
    return list(func(data))
'''

api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests = TESTS,
        checker = checker,
        function_name = {
            'python': 'visibilities',
            'js': 'visibilities'
            },
        cover_code = {
            'python-3': cover_iterable,
            #'js-node': 
            }
        ).on_ready
    )

