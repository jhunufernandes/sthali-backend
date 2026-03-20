"""{...}."""

from sthali_auth import APIKey, SthaliAuth
from sthali_auth import definitions as auth_definitions
from sthali_crud import SthaliCRUD
from sthali_db import definitions_type

from .config import config
from .models import ProjectModel
from .routers.root import ROOT
from .routers.views import VIEWS
from .schemas import ProjectSchemas


class SthaliBackend(SthaliCRUD):
    """{...}."""

    def __init__(self, definitions: definitions_type) -> None:
        """{...}."""
        dependencies = {}
        if "auth" in config.yaml_config:
            for _type, definition in config.yaml_config["auth"].items():
                client = SthaliAuth.from_type(_type, definition).client
                dependencies[_type] = client.dependency

            definitions += auth_definitions

            if "api_key" in config.yaml_config["auth"]:
                api_key = APIKey.from_type(**config.yaml_config["auth"]["api_key"])
                dependencies["api_key"] = api_key.dependency

        super().__init__(config, definitions, extended_routers=[VIEWS], dependencies=dependencies)
        root = ROOT()
        self.app.include_router(root.api_router)

definitions: definitions_type = [
    (ProjectModel, ProjectSchemas),
]  # type: ignore

sthali_backend = SthaliBackend(definitions)
app = sthali_backend.app
