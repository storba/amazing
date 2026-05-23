from config_parser import MazeConfig
from src.mazegen.maze_generator import MazeGenerator

PathMapDict = dict[tuple[int, int], tuple[str, int]]
COLS = ["\033[0m", "\033[94m", "\033[92m", "\033[96m", "\033[95m", "\033[91m"]
COLOR_NAMES = ["default", "blue", "green", "cyan", "magenta", "red"]


class MazeVisualizer:
    """Class for maze visualizing"""
    def __init__(
        self,
        maze: MazeGenerator,
        path: str,
        config: MazeConfig
    ) -> None:
        self.maze = maze
        self.path = path
        self.config = config

    def run_interactive(self) -> None:
        """Run the interactive terminal session for the maze.

        Generates the initial maze, draws it, then presents a menu loop that
        supports regeneration, path visibility toggling, colour cycling, and
        two animation modes.

        Args:
            config_path: Path to the configuration file.
        """
        show_path = True
        color_idx = 1

        def redraw() -> None:
            """Clear the terminal and redraw the maze with current settings."""
            print("\033[3J\033[2J\033[H", end="", flush=True)
            self.draw_maze_in_terminal(
                self.path if show_path else "",
                COLS,
                color_idx
            )

        def animation(num: int) -> None:
            """Animate the solution path step by step.

            Iterates over every arrow in the path, redrawing the maze on each
            frame with a 100 ms delay.

            Args:
                num: Animation mode passed to draw_maze_in_terminal (1 or 2).
            """
            import time
            path_len = len(self.path) - 1   # number of drawable arrows
            if path_len <= 0:
                return
            for i in range(path_len * 1):
                print("\033[3J\033[2J\033[H", end="", flush=True)
                self.draw_maze_in_terminal(
                    self.path if show_path else "",
                    COLS,
                    color_idx,
                    i % path_len,
                    num
                )
                time.sleep(0.1)
            redraw()
        redraw()
        while True:
            path_state = "ON" if show_path else "OFF"
            color_name = COLOR_NAMES[color_idx]
            print(
                f"\n 1. Regenerate  \n"
                f" 2. Show/hide path [{path_state}]  \n"
                f" 3. Rotate colors [{color_name}]  \n"
                f" 4. Animation1  \n"
                f" 5. Animation2  \n"
                f" 6. Quit"
            )
            choice = input("  Choice 1-6: ").strip()
            if choice == "1":
                redraw()
            elif choice == "2":
                show_path = not show_path
                redraw()
            elif choice == "3":
                color_idx = (color_idx + 1) % len(COLS)
                redraw()
            elif choice == "4":
                animation(1)
            elif choice == "5":
                animation(2)
            elif choice == "6" or choice == "q":
                break
            else:
                redraw()

    def draw_maze_in_terminal(
        self,
        path_str: str = "",
        colors: list[str] | None = None,
        color_idx: int = 0,
        anim: int = -1,
        anim_mode: int = 0
    ) -> None:
        if colors is None:
            raise ValueError("COLORS is required")
        RESET = "\033[0m" if colors else ""
        path_map = self._get_path_map(path_str) if path_str else {}
        if self.config.width is None:
            raise ValueError("WIDTH is required")
        if self.config.height is None:
            raise ValueError("HEIGHT is required")
        if self.config.entry is None:
            raise ValueError("ENTRY is required")
        if self.config.exit_m is None:
            raise ValueError("EXIT is required")
        if self.config.height < 7 or self.config.width < 9:
            print("Maze too small for 42")
        print(
            colors[color_idx]
            + "+"
            + "+".join("---" for _ in range(self.config.width))
            + "+"
        )
        for r in range(self.config.height):
            row_str = "|"
            for c in range(self.config.width):
                cell = self.maze.grid.get(r, c)
                if c == self.config.entry[0] and r == self.config.entry[1]:
                    row_str += RESET + "█S█" + colors[color_idx]
                elif c == self.config.exit_m[0] and r == self.config.exit_m[1]:
                    row_str += RESET + "█E█" + colors[color_idx]
                elif self.maze.is_42_cell(r, c):
                    row_str += (
                        colors[(color_idx + 1) % len(colors)]
                        + "███" + colors[color_idx]
                    )
                elif (r, c) in path_map:
                    arrow, path_idx = path_map[(r, c)]
                    if (anim_mode == 1):
                        if (path_idx == anim):
                            row_str += "\033[1;32m" + "███" + RESET
                        else:
                            row_str += RESET + arrow + colors[color_idx]
                    elif (anim_mode == 2):
                        if (path_idx <= anim):
                            row_str += RESET + arrow + colors[color_idx]
                        else:
                            row_str += "   " + colors[color_idx]
                    else:
                        row_str += RESET + arrow + colors[color_idx]
                else:
                    row_str += "   "
                row_str += " " if cell.east == 0 else colors[color_idx] + "|"
            print(row_str)
            bottom = colors[color_idx] + "+"
            for c in range(self.config.width):
                cell = self.maze.grid.get(r, c)
                bottom += (
                    "   " if cell.south == 0 else colors[color_idx]
                    + "---"
                )
                bottom += colors[color_idx] + "+"
            print(bottom)
        print(RESET)

    def _get_path_map(self, path_str: str) -> PathMapDict:
        """Перетворює рядок шляху на словник координат зі стрілочками."""
        if self.config.entry is None:
            raise ValueError("WIDTH is required")
        if self.config.exit_m is None:
            raise ValueError("HEIGHT is required")
        if self.config.width is None:
            raise ValueError("WIDTH is required")
        if self.config.height is None:
            raise ValueError("HEIGHT is required")
        c, r = self.config.entry[0], self.config.entry[1]
        path_dict = {}
        arrows = {"N": " ↑ ", "S": " ↓ ", "E": " → ", "W": " ← "}

        for i in range(len(path_str)):
            move = path_str[i]

            if move == "N":
                r -= 1
            elif move == "S":
                r += 1
            elif move == "E":
                c += 1
            elif move == "W":
                c -= 1

            if i + 1 < len(path_str):
                next_move = path_str[i + 1]
                path_dict[(r, c)] = (arrows[next_move], i)

        return path_dict
