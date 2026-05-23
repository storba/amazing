#!/usr/bin/env python3
import sys
from config_parser import MazeConfig
from maze_visualizer import MazeVisualizer
from src.mazegen.maze_generator import MazeGenerator


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
