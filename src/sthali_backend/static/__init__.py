from pathlib import Path

from fastapi.staticfiles import StaticFiles

static = StaticFiles(directory=str(Path(__file__).parent))
