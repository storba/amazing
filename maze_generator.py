from config_parser import MazeConfig
from dataclasses import dataclass
import random


@dataclass
class Cell():
    north: int = 1
    east: int = 1
    south: int = 1
    west: int = 1
    visited: bool = False
    def __str__(self) -> str:
        value = self.north | (self.east << 1) | (self.south << 2) | (self.west << 3)
        return format(value, 'X')

class CellGrid:
    """2D grid of Cell objects indexed by (row, col)."""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
    def get(self, row: int, col: int) -> Cell:
        """Return the Cell at position (row, col)."""
        return self.grid[row][col]
    def set(self, row: int, col: int, cell: Cell) -> None:
        """Set the Cell at position (row, col)."""
        self.grid[row][col] = cell
    def rm_wall(self, row: int, col: int, wall: int) -> tuple[int, int]:
        """ remove wall in CellGrid"""
        if wall == 0:
            self.grid[row][col].north = 0
            self.grid[row-1][col].south = 0
            return (row-1, col)
        elif wall == 1:
            self.grid[row][col].east = 0
            self.grid[row][col+1].west = 0
            return (row, col + 1)
        elif wall == 2:
            self.grid[row][col].south = 0
            self.grid[row+1][col].north = 0
            return (row+1, col)
        elif wall == 3:
            self.grid[row][col].west = 0
            self.grid[row][col-1].east = 0
            return (row, col-1)

class Maze():
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.grid = CellGrid(config.width, config.height)
        # self.entry = config.entry
        # self.exit = config.exit_m
        # self.perfect = config.perfect
        # self.seed = config.seed
        self.random = random.Random(self.config.seed)
        self.generate()
    def maze_random(self, row: int, col: int) -> int:
        if (row > 0 and row < self.config.width - 1 and col > 0 and col < self.config.height - 1):
            return(self.random.randrange(0,4))
        elif row == 0:
            if col == 0:
                return(self.random.randrange(1,3))
            elif col == self.config.height - 1:
                return(self.random.randrange(2,4))
            else:
                return(self.random.randrange(1,4))
        elif col == 0:
            if row == self.config.width - 1:
                return(self.random.randrange(0,2))
            else:
                return(self.random.randrange(0,3))
        elif col == self.config.height - 1:
            if row == self.config.width - 1:
                return(self.random.choice([0, 3]))
            else:
                return(self.random.choice([0, 2, 3]))
        elif row == self.config.width - 1:
            return(self.random.choice([0, 1, 3]))
    def generate(self) -> None:
        """Generate the maze."""
        stack = []
        row, col = self.config.entry[0], self.config.entry[1]
        self.grid.get(row, col).visited = True
        # self.draw_maze_in_terminal()
        while True:
            # find unvisited neighbors:
            neighbors = []
            if row > 0 and not self.grid.get(row-1, col).visited:
                neighbors.append((row-1, col, 0))  # north
            if col < self.config.width - 1 and not self.grid.get(row, col+1).visited:
                neighbors.append((row, col+1, 1))  # east
            if row < self.config.height - 1 and not self.grid.get(row+1, col).visited:
                neighbors.append((row+1, col, 2))  # south
            if col > 0 and not self.grid.get(row, col-1).visited:
                neighbors.append((row, col-1, 3))  # west
            
            if neighbors:
                stack.append((row, col))
                _, _, wall = self.random.choice(neighbors)
                row, col = self.grid.rm_wall(row, col, wall)
                self.grid.get(row, col).visited = True
            elif stack:
                row, col = stack.pop()  # backtrack
            else:
                break  # all cells visited
        # self.grid.get(self.config.entry[0], self.config.entry[1]).visited = True
        # row = self.config.entry[0]
        # col = self.config.entry[1]
        # print(f"row={row} col={col}")
        # while not (row == self.config.exit_m[0] and col ==self.config.exit_m[1]):
        #     i = self.maze_random(row , col)
        #     # print(f"i={i}")
        #     row, col = self.grid.rm_wall(row, col, i)
        #     self.grid.get(row, col).visited = True
        #     self.draw_maze_in_terminal()
        #     # print(f"row={row} col={col}")
        # self.grid.get(self.config.exit_m[0], self.config.exit_m[1]).visited = True

    def print_maze_tofile(self, filename: str) -> None:
        """Print the maze to a file."""
        with open(filename, 'w') as file:
            for row in self.grid.grid:
                file.write(''.join(str(cell) for cell in row))
                file.write('\n')
    def draw_maze_in_terminal(self) -> None:
        print('+' + '+'.join('---' for _ in range(self.config.width)) + '+')
        for r in range(self.config.height):
            row_str = '|'
            for c in range(self.config.width):
                cell = self.grid.get(r, c)
                row_str += '   '
                row_str += ' ' if cell.east == 0 else '|'
            print(row_str)
            bottom = '+'
            for c in range(self.config.width):
                cell = self.grid.get(r, c)
                bottom += '   ' if cell.south == 0 else '---'
                bottom += '+'
            print(bottom)