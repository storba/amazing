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
            A tuple of (MazeGenerator, solution_path) where solution_path is the
            BFS shortest path as a string of N/E/S/W letters.

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
        visualizer.run_interactive()
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
