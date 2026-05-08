@dataclass(frozen=True)
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algorithm: str = "backtracker"
    display: str = "ascii"