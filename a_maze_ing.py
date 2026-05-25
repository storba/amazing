#!/usr/bin/env python3
import sys
from config_parser import MazeConfig
from maze_visualizer import MazeVisualizer
from maze_generator import MazeGenerator


def build_maze(config: MazeConfig) -> tuple[MazeGenerator, str]:
    """Generate a maze from config, solve it, and write the output file.

    Args:
        config: Validated MazeConfig instance.

    Returns:
        A tuple of (MazeGenerator, solution_path) where solution_path is
        the BFS shortest path as a string of N/E/S/W letters.

    Raises:
        ValueError: If OUTPUT_FILE is not set in the config.
    """

    maze = MazeGenerator(
                        config.height,
                        config.width,
                        config.entry,
                        config.exit_m,
                        config.output_file,
                        config.perfect,
                        config.seed
                        )
    if not config.perfect:
        maze._make_imperfect()
    solution_path = maze.solve()
    if config.output_file is None:
        raise ValueError("OUTPUT_FILE is required")
    maze.print_maze_tofile(config.output_file, solution_path)
    return maze, solution_path


def main() -> None:
    """Entry point: parse the config file argument and start the session.

    Expects exactly one command-line argument: the path to a config file.
    All errors are caught and printed as a single message without a traceback.
    """
    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
    try:
        config = MazeConfig(sys.argv[1])
        maze, solution_path = build_maze(config)
        visualizer = MazeVisualizer(maze, solution_path, config)
        show_path = True
        color_idx = 1
        # visualizer.draw_maze_in_terminal(solution_path, color_idx)
        visualizer.redraw(show_path, color_idx)
        while True:
            path_state = "ON" if show_path else "OFF"
            color_name = visualizer.COLOR_NAMES[color_idx]
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
                config = MazeConfig(sys.argv[1])
                maze, solution_path = build_maze(config)
                visualizer = MazeVisualizer(maze, solution_path, config)
                visualizer.redraw(show_path, color_idx)
            elif choice == "2":
                show_path = not show_path
                visualizer.redraw(show_path, color_idx)
            elif choice == "3":
                color_idx = (color_idx + 1) % len(visualizer.COLS)
                visualizer.redraw(show_path, color_idx)
            elif choice == "4":
                visualizer.animation(1, show_path, color_idx)
            elif choice == "5":
                visualizer.animation(2, show_path, color_idx)
            elif choice == "6" or choice == "q":
                break
            else:
                visualizer.redraw(show_path, color_idx)

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


#############################################################
# from mazegenerator import MazeGenerator

# def print_maze_in_terminal(maze_gen: MazeGenerator) -> None:
#     """Виводить згенерований лабіринт у термінал."""
#     grid = maze_gen.maze
#     height = len(grid)
#     width = len(grid[0])
#     entry = maze_gen.maze_entry
#     exit_m = maze_gen.maze_exit
#     path_str = maze_gen.shortest_path

#     # 1. Перетворюємо рядок шляху на набір координат (x, y)
#     path_coords = set()
#     if isinstance(path_str, str) and path_str:
#         cx, cy = entry
#         for move in path_str:
#             if move == 'N': cy -= 1
#             elif move == 'S': cy += 1
#             elif move == 'E': cx += 1
#             elif move == 'W': cx -= 1
#             path_coords.add((cx, cy))
    
#     # Видаляємо вхід та вихід з точок шляху, щоб там малювалися 'S' та 'E'
#     path_coords.discard(entry)
#     path_coords.discard(exit_m)

#     # 2. Малюємо лабіринт рядок за рядком
#     for y in range(height):
#         # Малюємо верхні (Північні) стіни для поточного рядка
#         top_line = ""
#         for x in range(width):
#             top_line += "+"
#             # Бітова перевірка: 1 - North, 2 - East, 4 - South, 8 - West
#             if grid[y][x] & 1: 
#                 top_line += "---"
#             else:
#                 top_line += "   "
#         top_line += "+"
#         print(top_line)
        
#         # Малюємо ліві (Західні) стіни та "нутрощі" клітинки
#         mid_line = ""
#         for x in range(width):
#             if grid[y][x] & 8: # West wall
#                 mid_line += "|"
#             else:
#                 mid_line += " "
            
#             # Вміст клітинки
#             if (x, y) == entry:
#                 mid_line += " S "
#             elif (x, y) == exit_m:
#                 mid_line += " E "
#             elif grid[y][x] == 15: # Фігура 42 (fully closed: 1|2|4|8)
#                 mid_line += "███"
#             elif (x, y) in path_coords:
#                 mid_line += " • " # Шлях
#             else:
#                 mid_line += "   "
                
#         # Додаємо останню праву (Східну) стіну для крайньої правої клітинки
#         if grid[y][width - 1] & 2:
#             mid_line += "|"
#         else:
#             mid_line += " "
#         print(mid_line)
        
#     # 3. Малюємо нижні (Південні) стіни тільки для останнього рядка
#     bottom_line = ""
#     for x in range(width):
#         bottom_line += "+"
#         if grid[height - 1][x] & 4: # South wall
#             bottom_line += "---"
#         else:
#             bottom_line += "   "
#     bottom_line += "+"
#     print(bottom_line)


# # --- Твій оновлений скрипт запуску ---

# if __name__ == "__main__":
#     # Створюємо простий лабіринт 20x20. 
#     # Зверни увагу: передаємо кортеж size=(20, 20) згідно з твоїм __init__
#     maze_gen = MazeGenerator(size=(15, 15), entry_cell=(9, 9),perfect=False, seed=42)

#     # Виводимо технічну інформацію
#     print(f"Maze dimensions: {len(maze_gen.maze[0])}x{len(maze_gen.maze)}")
#     print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")
#     if isinstance(maze_gen.shortest_path, str):
#         print(f"Shortest path length: {len(maze_gen.shortest_path)}")
#     else:
#         print("No path found.")
        
#     print("\nВізуалізація лабіринту:\n")
#     print_maze_in_terminal(maze_gen)
