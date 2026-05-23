
class MazeConfig:
    """Configuration class for parsing and storing settings."""

    width: int | None = None
    height: int | None = None
    entry: tuple[int, int] | None = None
    exit_m: tuple[int, int] | None = None
    output_file: str | None = None
    perfect: bool | None = None
    seed: int | None = None

    def __init__(self, config_path: str) -> None:
        """Parse a KEY=VALUE configuration file and populate this instance.

        Lines starting with '#' and blank lines are ignored.  After parsing,
        validate_config() is called automatically.

        Args:
            config_path: Path to the plain-text configuration file.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read due to permissions.
            ValueError: If any line has invalid syntax or an unknown key.
        """
        try:
            with open(config_path) as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue

                    sep_idx = line.find("=")
                    if sep_idx == -1:
                        raise ValueError(f"Incorrect line format: '{line}'")
                    left_arg = line[:sep_idx].strip()
                    right_arg = line[sep_idx + 1:].strip()
                    self._parse_line(left_arg, right_arg, line)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{config_path}' does not exist")
        except PermissionError:
            raise PermissionError(f"Permission denied for '{config_path}'")

    def _parse_line(self, key: str, value: str, original_line: str) -> None:
        """Parse a single key-value pair and set the corresponding attribute.

        Args:
            key: The configuration key (e.g. 'WIDTH').
            value: The raw value string from the file.
            original_line: The original line text, used in error messages.

        Raises:
            ValueError: If the key is unknown, the value cannot be parsed, or
                coordinate format is incorrect.
        """
        try:
            if key == "WIDTH":
                self.width = int(value)
            elif key == "HEIGHT":
                self.height = int(value)
            elif key in ("ENTRY", "EXIT"):
                coords = value.split(",")
                if len(coords) != 2:
                    raise ValueError(
                        f"Incorrect coordinates: '{original_line}'"
                        )
                x_str = coords[0].strip()
                y_str = coords[1].strip()
                if not x_str or not y_str:
                    raise ValueError(
                        f"Missing coordinate value: '{original_line}'"
                        )
                parsed_coords = (int(x_str), int(y_str))
                if key == "ENTRY":
                    self.entry = parsed_coords
                else:
                    self.exit_m = parsed_coords
            elif key == "OUTPUT_FILE":
                self.output_file = value
            elif key == "PERFECT":
                if value == "True":
                    self.perfect = True
                elif value == "False":
                    self.perfect = False
                else:
                    raise ValueError(f"Unknown bool value: '{original_line}'")
            elif key == "SEED":
                self.seed = int(value)
            else:
                raise ValueError(f"Unknown parameter: '{original_line}'")
        except ValueError as e:
            raise ValueError(f"Invalid value in line '{original_line}': {e}")
