# mazegen — Maze Generator

**mazegen** is a reusable Python library for generating random mazes. It was created as part of the 42 curriculum by **svpanfil** and **dpohulia**.

The core class is `MazeGenerator`. It builds a maze from dimensions and entry/exit coordinates, optionally embeds a fixed **"42"** wall pattern, supports perfect and imperfect mazes, solves the shortest path with BFS, and writes the result to a text file.

---

## Requirements

- Python **3.9** or later
- No third-party dependencies (stdlib only)

---

## Installation

Install from the wheel or source archive in this folder:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or from the source distribution:

```bash
pip install mazegen-1.0.0.tar.gz
```

Recommended: use a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
pip install mazegen-1.0.0-py3-none-any.whl
```

---

## Quick start

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    height=16,
    width=40,
    entry=(0, 7),          # (col, row)
    exit_m=(39, 15),       # (col, row)
    output_file="output_maze.txt",
    perfect=True,          # True = perfect maze, False = call _make_imperfect()
    seed=32743,            # optional; omit or pass None for random
)

path = maze.solve()
maze.print_maze_tofile("output_maze.txt", path)
print(path)  # e.g. "EESSWN..."
```

For an **imperfect maze** (extra passages, multiple routes):

```python
maze = MazeGenerator(16, 40, (0, 7), (39, 15), "output_maze.txt", False, 42)
maze._make_imperfect()
path = maze.solve()
maze.print_maze_tofile("output_maze.txt", path)
```

---

## How it works

### Maze generation — recursive backtracker

`MazeGenerator` uses a **recursive backtracker** (randomised depth-first search):

1. Start at the entry cell and mark it visited.
2. Pick a random unvisited neighbour, remove the wall between them, and move there.
3. If no unvisited neighbours remain, backtrack along the stack.
4. Repeat until every reachable cell is visited.

This produces a **perfect maze**: exactly one path between any two points.

### "42" pattern

For mazes large enough (width ≥ 9, height ≥ 7), a fixed **"42"** shape is carved from fully walled cells in the centre. These cells are never opened during generation. Entry and exit must **not** lie inside the pattern.

### Imperfect mazes

When `perfect=False`, call `_make_imperfect()` after construction. Roughly **20 %** of remaining walls are randomly removed, with two constraints:

- No **3×3 fully open** areas are created.
- Walls touching the **"42"** pattern are never removed.

### Shortest path — BFS

`solve()` runs **breadth-first search** from entry to exit and returns the shortest path as a string of direction letters: `N`, `E`, `S`, `W`.

---

## Constructor parameters

| Parameter     | Type              | Required | Description |
|---------------|-------------------|----------|-------------|
| `height`      | `int`             | yes      | Number of rows (1–149) |
| `width`       | `int`             | yes      | Number of columns (1–299) |
| `entry`       | `(col, row)`      | yes      | Entry coordinates, must be inside the grid |
| `exit_m`      | `(col, row)`      | yes      | Exit coordinates, must differ from entry |
| `output_file` | `str`             | yes      | Output filename; must end with `.txt` |
| `perfect`     | `bool`            | yes      | `True` for a perfect maze; use `_make_imperfect()` when `False` |
| `seed`        | `int` or `None`   | no       | Random seed for reproducible mazes |

Validation runs in `__init__`. Invalid values raise `ValueError`.

---

## Public API

### `MazeGenerator`

| Method / attribute | Description |
|--------------------|-------------|
| `grid`             | `CellGrid` — 2D grid of `Cell` objects |
| `generate()`       | Called automatically in `__init__` |
| `solve()`          | Returns shortest path string (`N`/`E`/`S`/`W`) |
| `print_maze_tofile(filename, solution_path)` | Writes maze + metadata to a file |
| `_make_imperfect()` | Removes extra walls (call when `perfect=False`) |
| `is_42_cell(row, col)` | Returns whether a cell is part of the "42" pattern |

### Result structure — `list[list[Cell]]`

After `MazeGenerator` finishes, the maze is stored in `maze.grid` (`CellGrid`). The actual grid data is:

```python
maze.grid.grid: list[list[Cell]]   # height rows × width columns
```

Each `Cell` is a dataclass with four wall flags (default `1` = wall closed):

```python
@dataclass
class Cell:
    north: int = 1
    east: int = 1
    south: int = 1
    west: int = 1
    visited: bool = False
```

### `CellGrid`

```python
cell = maze.grid.get(row, col)   # row = y, col = x
maze.grid.set(row, col, cell)
cell = maze.grid.grid[row][col]  # direct access
```

### `Cell`

Each cell has four wall flags and a visited flag:

```python
cell.north   # 1 = wall closed, 0 = open
cell.east
cell.south
cell.west
cell.visited
str(cell)    # single hex digit encoding all four walls
```

Wall bits: **0 = North**, **1 = East**, **2 = South**, **3 = West**.

---

## Output file format

`print_maze_tofile()` writes:

1. **Maze body** — one row per line; each cell is one hexadecimal digit (wall encoding).
2. **Blank line**
3. **Entry** — `col,row`
4. **Exit** — `col,row`
5. **Solution** — shortest path as `N`/`E`/`S`/`W` letters

Example (abbreviated):

```
F3A9E...
...

0,7
39,15
EESSWN...
```

---

## Coordinate system

- **`entry` / `exit_m`** are passed as `(col, row)` — column first, then row.
- **`grid.get(row, col)`** uses `(row, col)` — row first, then column.

Keep this order consistent when accessing cells directly.

---

## Error handling

The library raises `ValueError` for:

- Missing or out-of-range dimensions
- Entry or exit outside the grid, or entry equal to exit
- Entry or exit inside the "42" pattern
- Output filename not ending in `.txt`

---

## Full example

```python
from mazegen import MazeGenerator

def build_and_save(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_m: tuple[int, int],
    output: str,
    perfect: bool = True,
    seed: int | None = None,
) -> str:
    maze = MazeGenerator(height, width, entry, exit_m, output, perfect, seed)
    if not perfect:
        maze._make_imperfect()
    path = maze.solve()
    maze.print_maze_tofile(output, path)
    return path

path = build_and_save(
    width=20,
    height=15,
    entry=(0, 0),
    exit_m=(19, 14),
    output="my_maze.txt",
    perfect=True,
    seed=42,
)
print(f"Shortest path ({len(path)} steps): {path}")
```

---

## Package contents

| File | Description |
|------|-------------|
| `mazegen/__init__.py` | Exports `MazeGenerator` |
| `mazegen/maze_generator.py` | Core generation, solving, and file output |

Import after installation:

```python
from mazegen import MazeGenerator
```

---

## Authors

- svpanfil — maze generation (recursive backtracker, perfect maze)
- dpohulia — BFS solver, imperfect maze generation

Project page: https://projects.intra.42.fr/a-maze-ing/dpohulia
