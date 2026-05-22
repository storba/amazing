*This project has been created as part of the 42 curriculum by svpanfil, dpohulia.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python 3. It reads a configuration file, generates a randomised maze, and writes the result to an output file in hexadecimal wall encoding. The maze is then displayed in the terminal with an interactive menu that lets you regenerate, show or hide the solution path, change colours, and watch an animated path walkthrough.

Key features:
- Perfect mazes (exactly one path between any two points) and imperfect mazes (extra passages, multiple routes)
- Embedded "42" pattern built from fully walled cells
- BFS shortest-path solver
- Reproducible generation via an optional seed
- Terminal rendering with ANSI colours and animation

## Instructions

### Requirements

- Python 3.10 or later
- `mypy`, `flake8` (for linting)

### Run

```bash
python3 a_maze_ing.py config.txt
```

`config.txt` is the configuration file (see format below). Any filename is accepted.

### Makefile targets

| Target | Action |
|--------|--------|
| `make install` | Install dependencies via pip |
| `make run` | Run the program with the default `config.txt` |
| `make debug` | Run with Python's built-in debugger (`pdb`) |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |
| `make lint` | Run `flake8` and `mypy` with recommended flags |
| `make lint-strict` | Run `flake8` and `mypy --strict` |

### Interactive menu

After the maze is drawn, the following options are available:

```
1. Regenerate          — generate a new random maze
2. Show/hide path      — toggle the solution path arrows
3. Rotate colors       — cycle the wall/path colour
4. Animation           — animate the solution path step by step
5. Quit
```

## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

| Key | Required | Description | Example |
|-----|----------|-------------|---------|
| `WIDTH` | yes | Number of cells horizontally | `WIDTH=40` |
| `HEIGHT` | yes | Number of cells vertically | `HEIGHT=16` |
| `ENTRY` | yes | Entry coordinates `x,y` (col,row) | `ENTRY=0,7` |
| `EXIT` | yes | Exit coordinates `x,y` (col,row) | `EXIT=39,15` |
| `OUTPUT_FILE` | yes | Output filename (must end in `.txt`) | `OUTPUT_FILE=output_maze.txt` |
| `PERFECT` | yes | `True` = perfect maze, `False` = imperfect | `PERFECT=False` |
| `SEED` | no | Integer seed for reproducible generation | `SEED=32743` |
| `DISPLAY` | no | `ascii` (default) or `window` | `DISPLAY=ascii` |

Default `config.txt` is included in the repository.

## Output file format

- One hexadecimal digit per cell, walls encoded as bits: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West. A `1` bit means the wall is closed.
- Cells stored row by row, one row per line.
- After an empty line: entry coordinates, exit coordinates, and the shortest path encoded as a sequence of `N`, `E`, `S`, `W` letters.

## Maze generation algorithm

The generator uses the **recursive backtracker** (randomised depth-first search):

1. Start at the entry cell, mark it visited.
2. Randomly pick an unvisited neighbour, remove the wall between them, move there.
3. If no unvisited neighbours exist, backtrack along the stack.
4. Repeat until all cells are visited.

This always produces a **perfect maze** — a spanning tree of the cell graph, guaranteeing exactly one path between any two points.

For **imperfect mazes** (`PERFECT=False`), roughly 20 % of the remaining walls are randomly removed after generation, subject to two constraints: no 3×3 open areas and no walls of the "42" pattern are touched.

**Why this algorithm?** The recursive backtracker is straightforward to implement and reason about, produces mazes with long winding corridors (good visual quality), and integrates naturally with the "42" pattern (pre-marked cells are simply treated as permanently visited).

## Reusable module

The maze generation logic lives entirely in `maze_generator.py` and is packaged as `mazegen-*` (`.whl` / `.tar.gz`) at the root of the repository.

### Installation

```bash
pip install mazegen-*.whl
```

### Basic usage

```python
from maze_generator import Maze
from config_parser import MazeConfig

config = MazeConfig("config.txt")   # load from file
maze = Maze(config)                 # generates a perfect maze immediately

# make it imperfect (optional)
maze._make_imperfect()

# solve — returns a string like "EESSWN..."
path = maze.solve()

# draw in terminal
maze.draw_maze_in_terminal(path)

# save to file
maze.print_maze_tofile("output.txt", path)
```

### Custom parameters

Edit `config.txt` or create a new one:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=my_maze.txt
PERFECT=True
SEED=42
```

### Accessing the structure

```python
cell = maze.grid.get(row, col)   # returns a Cell object
cell.north   # 1 = wall closed, 0 = open
cell.east
cell.south
cell.west
```

The solution is a plain string of cardinal letters (`N`, `E`, `S`, `W`) returned by `maze.solve()`.

## Team and project management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| **svpanfil** | Maze generation (recursive backtracker, perfect maze), terminal drawing |
| **dpohulia** | Configuration file parser, BFS path solver, imperfect maze generation, terminal drawing |

### Planning

We split the work by layer: svpanfil owned the core generation engine while dpohulia built the I/O and solving layer. Both contributed to the visual rendering and interactive menu. We iterated on the drawing code together, adding colour support and animation as bonuses toward the end.

### What worked well

- Clean separation between the generator module and the main script made it easy to work in parallel without merge conflicts.
- The recursive backtracker was fast to implement and easy to verify visually.
- ANSI colour animation required no extra dependencies.

### What could be improved

- The `MazeConfig` dataclass uses `| None` fields validated at runtime; using a stricter type-safe approach from the start would have eliminated several mypy warnings.
- More maze generation algorithms (Prim's, Kruskal's) could be added to compare visual styles.

### Tools used

- **Cursor** (AI-assisted IDE) — used for code suggestions, debugging hints, and reviewing logic
- **mypy** — static type checking
- **flake8** — style linting
- **Git** — version control and collaboration

## Resources

- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Think Labyrinth](https://www.astrolog.org/labyrnth/algrithm.htm)
- [BFS shortest path — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes reference](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python `dataclasses` documentation](https://docs.python.org/3/library/dataclasses.html)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

AI (Cursor / Claude) was used for:
- Suggesting the ANSI escape sequence for clearing the terminal scrollback buffer
- Debugging mypy `--strict` errors related to `tuple[int, int] | None` indexing
- Explaining why row/col coordinate order matters when calling `is_42_cell`

All AI-generated suggestions were reviewed, tested, and adapted by the team before being included in the project.

## Installation

Create virtual environment:
```shell
python3 -m venv .venv
```

Activate virtual environment:
```shell
source .venv/bin/activate
```

Install build dependency:
```shell
pip install build
```

Build mazegen package:
```shell
python -m build
```

Install mazgen package:
```
pip install dist/mazegen-0.0.1-py3-none-any.whl
```
