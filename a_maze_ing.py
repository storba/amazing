#!/usr/bin/env python3
import random
import sys
from config_parser import MazeConfig
from maze_generator import Maze
import os

COLORS      = ['',        '\033[94m', '\033[92m', '\033[96m', '\033[95m', '\033[91m']
COLOR_NAMES = ['default', 'blue',   'green',    'cyan',     'magenta',  'red'     ]

def print_config(cfg: MazeConfig) -> None:
    print(f"Width: {cfg.width}")
    print(f"Height: {cfg.height}")
    print(f"Entry: {cfg.entry[0]}, {cfg.entry[1]}")
    print(f"Exit: {cfg.exit_m[0]}, {cfg.exit_m[1]}")
    print(f"Output file: {cfg.output_file}")
    print(f"Perfect: {cfg.perfect}")
    print(f"Seed: {cfg.seed}")
    print(f"Display: {cfg.display}")

def build_maze(config: MazeConfig) -> tuple[Maze, str]:
    maze = Maze(config)
    if not config.perfect:
        maze._make_imperfect()
    solution_path = maze.solve()
    maze.print_maze_tofile(config.output_file, solution_path)
    return maze, solution_path
def run_interactive(config: MazeConfig) -> None:
    maze, solution_path = build_maze(config)
    show_path = True
    color_idx = 1
    def redraw() -> None:
        print('\033[3J\033[2J\033[H', end='', flush=True)
        maze.draw_maze_in_terminal(
            solution_path if show_path else '',
            COLORS[color_idx]
        )
    redraw()
    while True:
        path_state = 'ON' if show_path else 'OFF'
        color_name  = COLOR_NAMES[color_idx]
        print(f"\n  1. Regenerate  "
              f"2. Show/hide path [{path_state}]  "
              f"3. Rotate colors [{color_name}]  "
              f"4. Quit")
        choice = input("  Choice 1-4: ").strip()
        if choice == '1':
            maze, solution_path = build_maze(config)
            redraw()
        elif choice == '2':
            show_path = not show_path
            redraw()
        elif choice == '3':
            color_idx = (color_idx + 1) % len(COLORS)
            redraw()
        elif choice == '4':
            break


def main():
    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
    try:
        config = MazeConfig(sys.argv[1])
        run_interactive(config)
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
#need to read name of config file