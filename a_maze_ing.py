#!/usr/bin/env python3
import sys
from config_parser import MazeConfig
from mazegen.maze_generator import MazeGenerator

COLS = ["\033[0m", "\033[94m", "\033[92m", "\033[96m", "\033[95m", "\033[91m"]
COLOR_NAMES = ["default", "blue", "green", "cyan", "magenta", "red"]


def build_maze(config: MazeConfig) -> tuple[MazeGenerator, str]:
    """Generate a maze from config, solve it, and write the output file.

    Args:
        config: Validated MazeConfig instance.

    Returns:
        A tuple of (MazeGenerator, solution_path) where solution_path is the
        BFS shortest path as a string of N/E/S/W letters.

    Raises:
        ValueError: If OUTPUT_FILE is not set in the config.
    """
    maze = MazeGenerator(config)
    if not config.perfect:
        maze._make_imperfect()
    solution_path = maze.solve()
    if config.output_file is None:
        raise ValueError("OUTPUT_FILE is required")
    maze.print_maze_tofile(config.output_file, solution_path)
    return maze, solution_path


def run_interactive(config_path: str) -> None:
    """Run the interactive terminal session for the maze.

    Generates the initial maze, draws it, then presents a menu loop that
    supports regeneration, path visibility toggling, colour cycling, and
    two animation modes.

    Args:
        config_path: Path to the configuration file.
    """
    config = MazeConfig(config_path)
    maze, solution_path = build_maze(config)
    show_path = True
    color_idx = 1

    def redraw() -> None:
        """Clear the terminal and redraw the maze with current settings."""
        print("\033[3J\033[2J\033[H", end="", flush=True)
        maze.draw_maze_in_terminal(
            solution_path if show_path else "",
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
        path_len = len(solution_path) - 1   # number of drawable arrows
        if path_len <= 0:
            return
        for i in range(path_len * 1):
            print("\033[3J\033[2J\033[H", end="", flush=True)
            maze.draw_maze_in_terminal(
                solution_path if show_path else "",
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
            config = MazeConfig(config_path)
            maze, solution_path = build_maze(config)
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


def main() -> None:
    """Entry point: parse the config file argument and start the session.

    Expects exactly one command-line argument: the path to a config file.
    All errors are caught and printed as a single message without a traceback.
    """
    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
    try:
        run_interactive(sys.argv[1])
    except FileNotFoundError as e:
        print(e.args[0])
    except PermissionError as e:
        print(e.args[0])
    except ValueError as e:
        print(e.args[0])
    except Exception as e:
        print(e.args[0])


if __name__ == "__main__":
    main()
