from collections import defaultdict
from copy import deepcopy
from pprint import pprint

from constants import ADJACENT_DIRECTIONS
from helpers import coordinate_to_index, index_to_coordinate
from sortedcontainers import SortedList


class QueensState:
    def __init__(self, rows: int, cols: int, grid: dict, state: dict = None, queens: list = None):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.state = deepcopy(state) if state is not None else self.__build_state()
        self.color_frequency = self.__build_frequency()
        self.queens = queens.copy() if queens is not None else []

        # self.__print_grid()
        # print(self.rows, self.cols)
        # pprint(self.color_frequency)
    

    def __build_state(self):
        state = defaultdict(set)

        for coord, color in self.grid.items():
            state[color].add(coord)
        
        return state

    def __build_frequency(self):
        frequency_list = SortedList()

        for color, cells in self.state.items():
            frequency_list.add((len(cells), color))
        
        return frequency_list


    def __print_grid(self):
        output = []

        for r in range(self.rows):
            for c in range(self.cols):
                output.append(str(self.grid[(r, c)]))
            output.append('\n')
        
        print(''.join(output))
    

    def solve(self):
        # Invalid State Condition
        # At any point, number of empty colors become greater than queens placed, its invalid
        empty_colors = sum(1 for v in self.state.values() if not v)
        if empty_colors > len(self.queens):
            return False, None

        # (Phase - 1) Try to solve if there is any color with 1 cell 
        self.__solve_fixed()
        self.__remove_adjacent_common_cells()

        # By now we removed all cells with only 1 possibility
        # Check if solution is found, else proceed with Phase - 2
        solution_found = len(self.queens) == len(self.state)
        if solution_found:
            return solution_found, self.get_solution_forms()
    
        # (Phase - 2) Try to get all colors with only horizontal/vertical cells
        # Remove cells horizontally/vertically where queens cannot be placed
        straight_colors = self.__find_straight_cells()

        # Track already processed colors
        processed_colors = set()

        while straight_colors:
            color, index, orientation = straight_colors.pop()
            processed_colors.add(color)

            self.__remove_straight_cells(color, index, orientation)

            # It can happen that by removing some cells, some colors become straight again
            # Add straight colors to set again (if not already present)

            next_straight_colors = self.__find_straight_cells()
            for n_color, n_index, n_orientation in next_straight_colors:
                if n_color in processed_colors:
                    continue

                if n_color in straight_colors:
                    continue

                straight_colors.add((n_color, n_index, n_orientation))
            
            # It might happen that after removing some straight cells, some colors have 1 possiblity
            # Try to solve
            self.__solve_fixed()
            self.__remove_adjacent_common_cells()

        solution_found = len(self.queens) == len(self.state)
        if solution_found:
            return solution_found, self.get_solution_forms()

        # (Phase - 3) Now there are no staright colors, need to do some more analysis
        # There can be rows or columns where all cells are marked "x" except 1


        # (Phase - 4) Backtracking
        for _, color in self.color_frequency:
            if not self.state[color]:
                continue

            for coordinate in self.state[color]:
                bt_puzzle = QueensState(rows=self.rows, cols=self.cols, grid=self.grid, state=self.state, queens=self.queens)
                bt_puzzle.place_queen(coordinate=coordinate)
                is_solved, solution = bt_puzzle.solve()
                if not is_solved:
                    continue

                return True, solution
    
        return False, None
    

    def __solve_fixed(self):
        while self.color_frequency and self.color_frequency[0][0]==1:
            _, color = self.color_frequency.pop(0)
            
            coordinate = self.state[color].pop()
            self.place_queen(coordinate)
            
    

    # Public Method (for backtracking)
    def place_queen(self, coordinate: tuple):
        index = coordinate_to_index(coordinate=coordinate, cols=self.cols)
        self.queens.append(index)

        x, y = coordinate
        cells_to_remove = defaultdict(set)

        # Remove All Cells With Same Color
        for cell in self.state[self.grid[coordinate]]:
            cells_to_remove[self.grid[coordinate]].add(cell)

        # Remove Adjacent 8 Cells
        for dx, dy in ADJACENT_DIRECTIONS:
            r, c = (x + dx), (y + dy)

            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                continue
        
            color = self.grid[(r, c)]
            if (r, c) in self.state[color]:
                cells_to_remove[color].add((r, c))
        
        # Remove Row
        for c in range(self.cols):
            if c == y:
                continue

            color = self.grid[(x, c)]
            if (x, c) in self.state[color]:
                cells_to_remove[color].add((x, c))
        
        # Remove Column
        for r in range(self.rows):
            if r == x:
                continue
        
            color = self.grid[(r, y)]
            if (r, y) in self.state[color]:
                cells_to_remove[color].add((r, y))

        self.__remove_cells_and_update_frequency(cells_to_remove=cells_to_remove)


    def __check_straight(self, color: int):
        cells = self.state[color]
        if not cells:
            return False, None, None
        
        row_indexes = [r for r, _ in cells]
        column_indexes = [c for _, c in cells]
        
        if row_indexes and row_indexes.count(row_indexes[0]) == len(row_indexes):
            return True, row_indexes[0], 'h'
    
        if column_indexes and column_indexes.count(column_indexes[0]) == len(column_indexes):
            return True, column_indexes[0], 'v'
    
        return False, None, None


    def __find_straight_cells(self):
        straight_colors = set()

        for color in self.state.keys():
            is_straight, straight_index, orientation = self.__check_straight(color=color)
            if not is_straight:
                continue

            straight_colors.add((color, straight_index, orientation))
        
        return straight_colors


    def __remove_straight_cells(self, color: int, index: int, orientation: str):
        cells_to_remove = defaultdict(set)

        # If Orientation is "vertical", index is "column" index
        if orientation == 'v':
            c = index
            for r in range(self.rows):
                # Avoid Removing Same Color Cells
                if self.grid[(r, c)] == color:
                    continue

                # If cell is not present in color, skip
                if (r, c) not in self.state[self.grid[(r, c)]]:
                    continue

                cells_to_remove[self.grid[(r, c)]].add((r, c))
        else:
            r = index
            for c in range(self.cols):
                # Avoid Removing Same Color Cells
                if self.grid[(r, c)] == color:
                    continue

                # If cell is not present in color, skip
                if (r, c) not in self.state[self.grid[(r, c)]]:
                    continue

                cells_to_remove[self.grid[(r, c)]].add((r, c))
        
        self.__remove_cells_and_update_frequency(cells_to_remove=cells_to_remove)
    

    def __remove_cells_and_update_frequency(self, cells_to_remove: dict):
        for color, cells in cells_to_remove.items():
            previous_entry = (len(self.state[color]), color)
            self.color_frequency.remove(previous_entry)

            self.state[color] -= cells
            self.color_frequency.add((len(self.state[color]), color))
        
    
    def __remove_adjacent_common_cells(self):
        cells_to_remove = defaultdict(set)

        for color, cells in self.state.items():
            if not cells:
                continue
        
            common_cells = set.intersection(*[self.__get_adjacent_cells(coord) for coord in cells])
            for coordinate in common_cells:
                cells_to_remove[self.grid[coordinate]].add(coordinate)
            
        self.__remove_cells_and_update_frequency(cells_to_remove=cells_to_remove)
    

    def __get_adjacent_cells(self, coordinate: tuple):
        x, y = coordinate
        adjacent_cells = set()

        for dx, dy in ADJACENT_DIRECTIONS:
            r, c = (x + dx), (y + dy)
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                continue

            if self.grid[(r, c)] == self.grid[coordinate]:
                continue

            if (r, c) not in self.state[self.grid[(r, c)]]:
                continue
            
            adjacent_cells.add((r, c))
        
        return adjacent_cells


    def get_solution_forms(self):
        as_indexes = self.queens
        as_coordinates = [index_to_coordinate(index=index, cols=self.cols) for index in self.queens]
        return (as_indexes, as_coordinates)
