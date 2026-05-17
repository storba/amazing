#!/usr/bin/env python3
import random
import sys
from config_parser import MazeConfig
from maze_generator import Maze

def print_config(cfg: MazeConfig) -> None:
    print(f"Width: {cfg.width}")
    print(f"Height: {cfg.height}")
    print(f"Entry: {cfg.entry[0]}, {cfg.entry[1]}")
    print(f"Exit: {cfg.exit_m[0]}, {cfg.exit_m[1]}")
    print(f"Output file: {cfg.output_file}")
    print(f"Perfect: {cfg.perfect}")
    print(f"Seed: {cfg.seed}")
    print(f"Display: {cfg.display}")

def main():

    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
    try:
        config = MazeConfig(sys.argv[1])
        print_config(config)
    except FileNotFoundError as e:
        print(e.args[0])
    except PermissionError:
        print(e.args[0])
    except ValueError as e:
        print(e.args[0])
    except Exception as e:
        print(e.args[0])
    maze = Maze(config)
    maze.print_maze_tofile(config.output_file)
    solution_path = maze.solve()
    maze.draw_maze_in_terminal(solution_path)
if __name__ == "__main__":
    main()
#need to read name of config file