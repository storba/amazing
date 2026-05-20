#!/usr/bin/env python3
import sys
from config_parser import MazeConfig
from maze_generator import Maze

COLS = ["\033[0m", "\033[94m", "\033[92m", "\033[96m", "\033[95m", "\033[91m"]
COLOR_NAMES = ["default", "blue", "green", "cyan", "magenta", "red"]


def build_maze(config: MazeConfig) -> tuple[Maze, str]:
    maze = Maze(config)
    if not config.perfect:
        maze._make_imperfect()
    solution_path = maze.solve()
    if config.output_file is None:
        raise ValueError("OUTPUT_FILE is required")
    maze.print_maze_tofile(config.output_file, solution_path)
    return maze, solution_path


def run_interactive(config_path: str) -> None:
    config = MazeConfig(config_path)
    maze, solution_path = build_maze(config)
    show_path = True
    color_idx = 1

    def redraw() -> None:
        print("\033[3J\033[2J\033[H", end="", flush=True)
        maze.draw_maze_in_terminal(
            solution_path if show_path else "",
            COLS,
            color_idx
        )

    redraw()
    while True:
        path_state = "ON" if show_path else "OFF"
        color_name = COLOR_NAMES[color_idx]
        print(
            f"\n  1. Regenerate  "
            f"2. Show/hide path [{path_state}]  "
            f"3. Rotate colors [{color_name}]  "
            f"4. Quit"
        )
        choice = input("  Choice 1-4: ").strip()
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
        elif choice == "4" or choice == "q":
            break


def main() -> None:
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
