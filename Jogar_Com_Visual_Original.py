
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from visual_original_extra.iniciar import executar

if __name__ == "__main__":
    executar(Path(__file__).resolve().parent)
