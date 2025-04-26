import os
from pathlib import Path

import pytest

from app.html_parser import QueensHtmlParser
from app.solver import QueensState


def test_grids_exist():
    for map_number in range(1, 100+1):
        file_name = f'queens-game-grid-{map_number}.html'
        path = os.path.join(Path(os.getcwd()), 'tests', 'test-grids', file_name)
        assert os.path.exists(path), f"Grid {map_number} not found"


@pytest.mark.parametrize("map_number", list(range(1, 100+1)))
def test_grids(map_number):
    file_name = f'queens-game-grid-{map_number}.html'
    path = os.path.join(Path(os.getcwd()), 'tests', 'test-grids', file_name)

    with open(path, 'r') as in_file:
        html = in_file.read()
    
    parser = QueensHtmlParser(source='Queens Game')
    rows, cols, grid = parser.parse_queens_html(html)
    puzzle = QueensState(rows=rows, cols=cols, grid=grid)
    is_solved, _ = puzzle.solve()
    assert is_solved == True


def test_extras_1():
    rows = 9
    cols = 9
    grid = {
        (0, 0): 6,
        (0, 1): 6,
        (0, 2): 6,
        (0, 3): 6,
        (0, 4): 6,
        (0, 5): 6,
        (0, 6): 5,
        (0, 7): 5,
        (0, 8): 5,
        (1, 0): 6,
        (1, 1): 6,
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 1,
        (1, 5): 1,
        (1, 6): 1,
        (1, 7): 2,
        (1, 8): 5,
        (2, 0): 6,
        (2, 1): 6,
        (2, 2): 1,
        (2, 3): 11,
        (2, 4): 11,
        (2, 5): 11,
        (2, 6): 1,
        (2, 7): 2,
        (2, 8): 2,
        (3, 0): 6,
        (3, 1): 6,
        (3, 2): 1,
        (3, 3): 11,
        (3, 4): 0,
        (3, 5): 11,
        (3, 6): 1,
        (3, 7): 3,
        (3, 8): 2,
        (4, 0): 6,
        (4, 1): 6,
        (4, 2): 1,
        (4, 3): 0,
        (4, 4): 0,
        (4, 5): 11,
        (4, 6): 1,
        (4, 7): 3,
        (4, 8): 2,
        (5, 0): 6,
        (5, 1): 6,
        (5, 2): 1,
        (5, 3): 11,
        (5, 4): 11,
        (5, 5): 11,
        (5, 6): 1,
        (5, 7): 3,
        (5, 8): 3,
        (6, 0): 6,
        (6, 1): 8,
        (6, 2): 1,
        (6, 3): 1,
        (6, 4): 1,
        (6, 5): 1,
        (6, 6): 1,
        (6, 7): 4,
        (6, 8): 3,
        (7, 0): 6,
        (7, 1): 8,
        (7, 2): 1,
        (7, 3): 1,
        (7, 4): 1,
        (7, 5): 1,
        (7, 6): 1,
        (7, 7): 4,
        (7, 8): 4,
        (8, 0): 8,
        (8, 1): 8,
        (8, 2): 8,
        (8, 3): 8,
        (8, 4): 8,
        (8, 5): 4,
        (8, 6): 4,
        (8, 7): 4,
        (8, 8): 4,
    }
    puzzle = QueensState(rows=rows, cols=cols, grid=grid)
    is_solved, _ = puzzle.solve()
    assert is_solved == True
