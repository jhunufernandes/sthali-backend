"""{...}."""

from sthali_auth import ConfigSchema as AuthConfigSchema
from sthali_core.config import Config as BaseConfig
from sthali_crud.config import ConfigSchema as BaseConfigSchema


class ConfigSchema(AuthConfigSchema, BaseConfigSchema):
    """{...}."""


class Config(BaseConfig):
    """{...}."""
    config_schema = ConfigSchema

    def __init__(self, config_file_path: str) -> None:
        """{...}."""
        super().__init__(config_file_path)


config = Config.load()
