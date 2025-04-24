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
