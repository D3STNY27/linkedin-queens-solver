import re

from bs4 import BeautifulSoup
from constants import QUEENS_GRID_ID
from helpers import index_to_coordinate


class QueensHtmlParser:
    def __init__(self, source: str):
        self.source = source


    def parse_queens_html(self, html: str):
        func_map = {
            'Queens Game': self.__parse_queens_game,
            'Linkedin Queens': self.__parse_linkedin_queens
        }
        return func_map[self.source](html=html)


    def __parse_linkedin_queens(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        
        outer_div = soup.find(id=QUEENS_GRID_ID)
        outer_div_attrs = outer_div.attrs
        tokens = outer_div_attrs['style'].replace('--', '').replace(';', '').split()
        
        rows = int(tokens[1]) if tokens[0] == 'rows' else int(tokens[3])
        cols = int(tokens[3]) if tokens[2] == 'cols' else int(tokens[1])
        grid = {}

        for children in outer_div.find_all("div", attrs={"role": "button"}):
            attrs = children.attrs

            if 'cell-color' not in attrs['class'][1]:
                continue
        
            cell_idx = int(attrs['data-cell-idx'])
            cell_color = attrs['class'][1]
            cell_color_int = int(cell_color.replace('cell-color-', ''))

            r, c = index_to_coordinate(cell_idx, cols)

            grid[(r, c)] = cell_color_int
        
        if len(grid) != rows * cols:
            raise Exception('Invalid Queens Grid')
        
        return rows, cols, grid


    def __parse_queens_game(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        
        outer_div = soup.find(id='grid')
        outer_div_attrs = outer_div.attrs
        
        row_num_match = re.search(r'grid-template-rows:\s*repeat\((\d+),', outer_div_attrs['style'])
        col_num_match = re.search(r'grid-template-columns:\s*repeat\((\d+),', outer_div_attrs['style'])

        rows = int(row_num_match.group(1))
        cols = int(col_num_match.group(1))
        grid = {}
        
        color_index = 0
        rgb_map = {}

        for r in range(rows):
            for c in range(cols):
                div = outer_div.find_all("div", attrs={"id": f"case-{r}-{c}"})
                attrs = div[0].attrs
                color = attrs['style'].replace('background-color: ', '')

                if color not in rgb_map:
                    rgb_map[color] = color_index
                    grid[(r, c)] = color_index
                    color_index += 1
                else:
                    grid[(r, c)] = rgb_map[color]
        
        if len(grid) != rows * cols:
            raise Exception('Invalid Queens Grid')
        
        return rows, cols, grid
