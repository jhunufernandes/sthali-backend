from pathlib import Path

from fastapi.templating import Jinja2Templates
from sthali_crud.config import get_context_processors


class Templates:
    def __init__(self, directory: str | list[str] | None = None, context_processors: list | None = None):
        self.directory = directory or str(Path(__file__).parent)
        self.context_processors = context_processors or [get_context_processors]
        self.templates = Jinja2Templates(directory=self.directory, context_processors=self.context_processors)

    def get_templates(self):
        return self.templates
