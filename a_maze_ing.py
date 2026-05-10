#!/usr/bin/env python3
import random
import sys
from config_parser import MazeConfig
from maze_generator import Maze
# cfg = MazeConfig(
#     width=20,
#     height=15,
#     entry=(0, 0),
#     exit_=(19, 14),
#     output_file="maze.txt",
#     perfect=True,
#     seed=42,
# )
# maze = Maze(cfg)

def main():

    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
    try:
        config = MazeConfig(sys.argv[1])
    except FileNotFoundError as e:
        print(e.args[0])
    except PermissionError:
        print(e.args[0])
    except Exception as e:
        print(e.args[0])
if __name__ == "__main__":
    main()
#need to read name of config file