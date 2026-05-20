from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).with_name("src")))

from bytenoise.app import main


main()
