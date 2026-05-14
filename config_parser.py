from dataclasses import dataclass

#@dataclass(frozen=True)
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
						raise Exception(f"Incorrect line: '{line.strip()}'")
					left_arg = line[:sep_idx].strip()
					right_arg = line[sep_idx + 1:].strip()
					try:
						if left_arg == "WIDTH" and int(right_arg) > 0 and int(right_arg) < 300:
							self.width = int(right_arg)
						elif left_arg == "HEIGHT" and int(right_arg) > 0 and int(right_arg) < 150:
							self.height = int(right_arg)
						elif (left_arg == "ENTRY" or left_arg == "EXIT"):
							if (right_arg.find(",") == -1):
								raise Exception(f"Incorrect coordinates format: {line.strip()}")
							coords = right_arg.split(",")
							if (len(coords) != 2):
								raise ValueError(f"Incorrect coordinates: '{line.strip()}'.")
							tuple_coords = (int(coords[0].strip()), int(coords[1].strip()))
							if not check_coords_range(tuple_coords, self):
									raise Exception(f"Incorrect coordinates range:'{line.strip()}'")
							if left_arg == "ENTRY":
								self.entry = tuple_coords
							else:
								self.exit_m = tuple_coords
						elif left_arg == "OUTPUT_FILE":
							self.output_file = right_arg
						elif left_arg == "PERFECT":
							if right_arg == "True":
								self.perfect = True
							elif right_arg == "False":
								self.perfect = False
							else:
								raise Exception(f"Unknown bool value:'{line.strip()}'")
						elif left_arg == "SEED":
							self.seed = int(right_arg)
						elif left_arg == "DISPLAY":
							if not(right_arg == "ascii" or right_arg == "window"):
								raise Exception(f"Unknown display type:'{line.strip()}'")
							self.display = right_arg
						else:
							raise Exception(f"Unknown line: '{line.strip()}'.")
					except ValueError:
						raise ValueError(f"Incorrect value in line: '{line.strip()}'")
					except Exception as e:
						raise e
					#print(line)
		except FileNotFoundError:
			raise FileNotFoundError(f"File '{config_path}' does not exist")
		except PermissionError:
			raise PermissionError(f"File '{config_path}' exist, but you dont have correct permitions")
		except ValueError as e:
			raise e
		except Exception as e:
			raise e
	def validate_config(self) -> None:
		pass

def check_coords_range(coords: tuple, cfg: MazeConfig) -> bool:
	if not coords[0] in range(0, cfg.width + 1):
		return False
	if not coords[1] in range(0, cfg.height + 1):
		return False
	return True

# def main():
# 	MazeConfig("config.txt")

# if __name__ == "__main__":
#     main()