import sys
from pathlib import Path
from pprint import pprint

from parser import parse


data = parse(Path(sys.argv[1]))
pprint(data)
