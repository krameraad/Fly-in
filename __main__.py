import sys
from pathlib import Path

# from zone import Zone
from parser import parse
from builder import build


data = parse(Path(sys.argv[1]))
zones = build(data)
start, end = data['start_hub']['name'], data['end_hub']['name']


print(f"\033[1m{'Zone':<24} {'x':>4} {'y':>4} {'Type':<12} "
      f"{'Color':<6} {'Capacity'}\033[0m\n",
      '\033[2m', "-" * 63, '\033[0m', sep='')
for k, v in zones.items():
    print(v)
