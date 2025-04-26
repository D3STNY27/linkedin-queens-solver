import os

os.system('cls')

import questionary
from constants import QUEENS_SOURCES
from driver import ChromeDriver
from html_parser import QueensHtmlParser
from solver import QueensState

# Ask Queens Game Source
source = questionary.select(
    "Queens Source:",
    choices=QUEENS_SOURCES
).ask()


# User Cancel Termination
if source is None:
    exit(0)


driver = ChromeDriver(source=source)
queens_html = driver.fetch_queens_grid_html()

parser = QueensHtmlParser(source=source)
rows, cols, grid = parser.parse_queens_html(html=queens_html)

puzzle = QueensState(rows=rows, cols=cols, grid=grid)
solution_found, solution = puzzle.solve()

if not solution_found:
    raise Exception('Solution Not Found')

print(f'{solution=}')
driver.put_solution_to_grid(solution)
