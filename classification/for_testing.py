from pathlib import Path

# current_dir = Path.cwd()
dir = Path("/".join(Path.cwd().parts[:-1])) / "data"

#print(dir)

print(Path.cwd() / "data" / "data")