from dataclasses import dataclass
from collections import deque
import random


@dataclass
class Cell:
    north: int = 1
    east: int = 1
    south: int = 1
    west: int = 1
    visited: bool = False

    def __str__(self) -> str:
        value = (self.north | (self.east << 1)
                 | (self.south << 2) | (self.west << 3))
        return format(value, "X")


class CellGrid:
    """2D grid of Cell objects indexed by (row, col)."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

    def get(self, row: int, col: int) -> Cell:
        """Return the Cell at position (row, col)."""
        return self.grid[row][col]

    def set(self, row: int, col: int, cell: Cell) -> None:
        """Set the Cell at position (row, col)."""
        self.grid[row][col] = cell

    def rm_wall(self, row: int, col: int, wall: int) -> tuple[int, int]:
        """Remove wall in CellGrid"""
        if wall == 0:
            self.grid[row][col].north = 0
            self.grid[row - 1][col].south = 0
            return (row - 1, col)
        elif wall == 1:
            self.grid[row][col].east = 0
            self.grid[row][col + 1].west = 0
            return (row, col + 1)
        elif wall == 2:
            self.grid[row][col].south = 0
            self.grid[row + 1][col].north = 0
            return (row + 1, col)
        elif wall == 3:
            self.grid[row][col].west = 0
            self.grid[row][col - 1].east = 0
            return (row, col - 1)
        else:
            return (0, 0)

    def restore_wall(self, row: int, col: int, wall: int) -> None:
        """Restore wall in CellGrid"""
        if wall == 0:
            self.grid[row][col].north = 1
            self.grid[row - 1][col].south = 1
        elif wall == 1:
            self.grid[row][col].east = 1
            self.grid[row][col + 1].west = 1
        elif wall == 2:
            self.grid[row][col].south = 1
            self.grid[row + 1][col].north = 1
        elif wall == 3:
            self.grid[row][col].west = 1
            self.grid[row][col - 1].east = 1


class MazeGenerator:
    def __init__(
        self,
        height: int | None,
        width: int | None,
        entry: tuple[int, int] | None,
        exit_m: tuple[int, int] | None,
        output_file: str | None,
        perfect: bool | None,
        seed: int | None
    ) -> None:
        if width is None:
            raise ValueError("WIDTH is required")
        if height is None:
            raise ValueError("HEIGHT is required")
        if entry is None:
            raise ValueError("ENTRY is required")
        if exit_m is None:
            raise ValueError("EXIT is required")
        if output_file is None:
            raise ValueError("OUTPUT_FILE is required")
        if perfect is None:
            raise ValueError("PERFECT is required")
        # if seed is None:
        #     seed = None

        self.grid = CellGrid(width, height)
        self.height = height
        self.width = width
        self.entry = entry
        self.exit_m = exit_m
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.random = random.Random(seed)
        self.generate()

    def maze_random(self, row: int, col: int) -> int:
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        if (
            row > 0
            and row < self.width - 1
            and col > 0
            and col < self.height - 1
        ):
            return self.random.randrange(0, 4)
        elif row == 0:
            if col == 0:
                return self.random.randrange(1, 3)
            elif col == self.height - 1:
                return self.random.randrange(2, 4)
            else:
                return self.random.randrange(1, 4)
        elif col == 0:
            if row == self.width - 1:
                return self.random.randrange(0, 2)
            else:
                return self.random.randrange(0, 3)
        elif col == self.height - 1:
            if row == self.width - 1:
                return self.random.choice([0, 3])
            else:
                return self.random.choice([0, 2, 3])
        elif row == self.width - 1:
            return self.random.choice([0, 1, 3])
        else:
            return 0

    FORTY_TWO = {
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2),  # "4"
        (0, 4), (0, 5), (0, 6), (1, 6), (2, 4), (2, 5), (2, 6),
        (3, 4), (4, 4), (4, 5), (4, 6),  # "2"
    }

    def is_42_cell(self, row: int, col: int) -> bool:
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        if self.height < 7 or self.width < 9:
            return False
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2
        return (row - start_row, col - start_col) in self.FORTY_TWO

    def generate(self) -> None:
        """Generate the maze."""
        stack = []
        if self.entry is None:
            raise ValueError("ENTRY is required")
        col, row = self.entry[0], self.entry[1]
        self.grid.get(row, col).visited = True
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        if (self.is_42_cell(self.entry[1], self.entry[0])):
            raise ValueError("ENTRY should not be inside 42")
        if self.exit_m is None:
            raise ValueError("EXIT is required")
        if (self.is_42_cell(self.exit_m[1], self.exit_m[0])):
            raise ValueError("EXIT should not be inside 42")
        for r in range(self.height):
            for c in range(self.width):
                if self.is_42_cell(r, c):
                    self.grid.get(r, c).visited = True
        while True:
            # find unvisited neighbors:
            neighbors = []
            if (
                row > 0
                and not self.grid.get(row - 1, col).visited
                and not self.is_42_cell(row - 1, col)
            ):
                neighbors.append((row - 1, col, 0))  # north
            if (
                col < self.width - 1
                and not self.grid.get(row, col + 1).visited
                and not self.is_42_cell(row, col + 1)
            ):
                neighbors.append((row, col + 1, 1))  # east
            if (
                row < self.height - 1
                and not self.grid.get(row + 1, col).visited
                and not self.is_42_cell(row + 1, col)
            ):
                neighbors.append((row + 1, col, 2))  # south
            if (
                col > 0
                and not self.grid.get(row, col - 1).visited
                and not self.is_42_cell(row, col - 1)
            ):
                neighbors.append((row, col - 1, 3))  # west

            if neighbors:
                stack.append((row, col))
                _, _, wall = self.random.choice(neighbors)
                row, col = self.grid.rm_wall(row, col, wall)
                self.grid.get(row, col).visited = True
            elif stack:
                row, col = stack.pop()  # backtrack
            else:
                break  # all cells visited

    def print_maze_tofile(self, filename: str, solution_path: str) -> None:
        """Print the maze to a file."""
        if self.entry is None:
            raise ValueError("ENTRY is required")
        if self.exit_m is None:
            raise ValueError("EXIT is required")
        try:
            with open(filename, "w") as file:
                for row in self.grid.grid:
                    file.write("".join(str(cell) for cell in row))
                    file.write("\n")
                file.write("\n")
                file.write(f"{self.entry[0]},"
                           f"{self.entry[1]}\n")
                file.write(f"{self.exit_m[0]},"
                           f"{self.exit_m[1]}\n")
                file.write(solution_path + "\n")
        except Exception as e:
            print(f"Output_file error: {e}")

    def solve(self) -> str:
        """Finds the shortest path from entry to exit using BFS."""
        if self.entry is None:
            raise ValueError("WIDTH is required")
        if self.exit_m is None:
            raise ValueError("HEIGHT is required")
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        start_col, start_row = self.entry
        target_col, target_row = self.exit_m
        queue = deque([(start_row, start_col, "")])

        visited = set()
        visited.add((start_row, start_col))

        while queue:
            r, c, path = queue.popleft()
            if r == target_row and c == target_col:
                return path
            cell = self.grid.get(r, c)
            if (
                r > 0
                and cell.north == 0
                and (r - 1, c) not in visited
                and not self.is_42_cell(r - 1, c)
            ):
                visited.add((r - 1, c))
                queue.append((r - 1, c, path + "N"))
            if (
                c < self.width - 1
                and cell.east == 0
                and (r, c + 1) not in visited
                and not self.is_42_cell(r, c + 1)
            ):
                visited.add((r, c + 1))
                queue.append((r, c + 1, path + "E"))
            if (
                r < self.height - 1
                and cell.south == 0
                and (r + 1, c) not in visited
                and not self.is_42_cell(r + 1, c)
            ):
                visited.add((r + 1, c))
                queue.append((r + 1, c, path + "S"))
            if (
                c > 0
                and cell.west == 0
                and (r, c - 1) not in visited
                and not self.is_42_cell(r, c - 1)
            ):
                visited.add((r, c - 1))
                queue.append((r, c - 1, path + "W"))

        return "No valid path found"

    def _is_3x3_open(self, tr: int, tc: int) -> bool:
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        if (
            tr < 0
            or tr + 2 >= self.height
            or tc < 0
            or tc + 2 >= self.width
        ):
            return False

        for r in range(tr, tr + 3):
            for c in range(tc, tc + 2):
                if self.grid.get(r, c).east != 0:
                    return False

        for r in range(tr, tr + 2):
            for c in range(tc, tc + 3):
                if self.grid.get(r, c).south != 0:
                    return False
        return True

    def _causes_3x3_open(
        self, r: int, c: int, neighbor_r: int, neighbor_c: int
    ) -> bool:
        """Checks for 3x3 areas after removing the wall"""
        min_r = min(r, neighbor_r) - 2
        max_r = max(r, neighbor_r)
        min_c = min(c, neighbor_c) - 2
        max_c = max(c, neighbor_c)

        for tr in range(min_r, max_r + 1):
            for tc in range(min_c, max_c + 1):
                if self._is_3x3_open(tr, tc):
                    return True
        return False

    def _make_imperfect(self) -> None:
        """Randomly deletes walls to make maze imperfect"""
        if self.width is None:
            raise ValueError("WIDTH is required")
        if self.height is None:
            raise ValueError("HEIGHT is required")
        walls_to_break = (self.width * self.height) * 0.2

        broken = 0
        attempts = 0
        max_attempts = walls_to_break * 10

        while broken < walls_to_break and attempts < max_attempts:
            attempts += 1

            r = self.random.randrange(0, self.height - 1)
            c = self.random.randrange(0, self.width - 1)

            if self.is_42_cell(r, c):
                continue

            wall_to_break = self.random.randrange(4)
            cell = self.grid.get(r, c)
            if wall_to_break == 0 and r == 0:       # would remove top border
                continue
            if wall_to_break == 3 and c == 0:       # would remove left border
                continue

            if (
                (wall_to_break == 0 and cell.north == 0)
                or (wall_to_break == 1 and cell.east == 0)
                or (wall_to_break == 2 and cell.south == 0)
                or (wall_to_break == 3 and cell.west == 0)
            ):
                continue

            neighbor_r, neighbor_c = self.grid.rm_wall(r, c, wall_to_break)

            if self.is_42_cell(neighbor_r, neighbor_c):
                self.grid.restore_wall(r, c, wall_to_break)
            if self._causes_3x3_open(r, c, neighbor_r, neighbor_c):
                self.grid.restore_wall(r, c, wall_to_break)
            else:
                broken += 1
