LINKEDIN_QUEENS_URL = 'https://www.linkedin.com/games/queens/'
QUEENS_GAME_URL = 'https://www.queens-game.com/'

QUEENS_SOURCES = [
    'Queens Game',
    'Linkedin Queens'
]

SOURCE_TO_URL_MAP = {
    'Queens Game': QUEENS_GAME_URL,
    'Linkedin Queens': LINKEDIN_QUEENS_URL
}

SOLVE_PUZZLE_BUTTON_ID = 'launch-footer-start-button'
PUZZLE_IFRAME_CSS = 'iframe.game-launch-page__iframe'
QUEENS_GRID_ID = 'queens-grid'
GRID_CELL_ID = 'div[role="button"][data-cell-idx="{index}"]'

ADJACENT_DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]