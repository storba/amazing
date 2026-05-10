#!/usr/bin/env python3
import random
from config_parser import MazeConfig
from maze_generator import Maze
cfg = MazeConfig(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42,
)
maze = Maze(cfg)

def main():
    order: list[int] = [0, 1, 2, 3]
    a = random.Random(None)
    print(order)
    for i in range(1, 11):
       print(f"None, {a.choice([1,2])}")
        #a.shuffle(order)
        #print(f"None, random={order}")
    a = random.Random(1)
    print()
    order: list[int] = [0, 1, 2, 3]
    print(order)
    for i in range(1, 11):
        a.shuffle(order)
        print(f"1, random={order}")
    a = random.Random(1)
    print()
    order: list[int] = [0, 1, 2, 3]
    print(order)
    for i in range(1, 11):
        a.shuffle(order)
        print(f"1, random={order}")
    a = random.Random(2)
    print()
    order: list[int] = [0, 1, 2, 3]
    print(order)
    for i in range(1, 11):
        a.shuffle(order)
        print(f"2, random={order}")
    a = random.Random(11)
    print()
    order: list[int] = [0, 1, 2, 3]
    print(order)
    for i in range(1, 11):
        a.shuffle(order)
        print(f"11, random={order}")
    a = random.Random(100)
    print()
    order: list[int] = [0, 1, 2, 3]
    print(order)
    for i in range(1, 11):
        a.shuffle(order)
        print(f"100, random={order}")
if __name__ == "__main__":
    main()
#need to read name of config file 