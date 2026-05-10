from dataclasses import dataclass

@dataclass(frozen=True)
class MazeConfig:
	"""
	Configuration class for parsing and storing settings.
	"""
	width: int
	height: int
	entry: tuple[int, int]
	exit_m: tuple[int, int]
	output_file: str
	perfect: bool
	seed: int | None = None
	display: str = "ascii"
	def __init__(self, config_path: str) -> None:
		try:
			with open(config_path) as file:
				for line in file.readlines():
					if line.strip().startswith("#") or len(line.strip()) == 0:
						continue
					sep_idx = line.find("=")
					if sep_idx == -1:
						raise Exception(f"Incorrect line: {line}")
					print(line)
		except FileNotFoundError:
			raise FileNotFoundError(f"File '{config_path}' does not exist")
		except PermissionError:
			raise PermissionError(f"File '{config_path}' exist, but you dont have correct permitions")
		except Exception as e:
			raise e

# def main():
# 	MazeConfig("config.txt")

# if __name__ == "__main__":
#     main()