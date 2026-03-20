"""View handlers for rendering HTML templates for CRUD operations."""
from collections.abc import Callable
from typing import Any, get_args, get_origin
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sthali_crud.dependencies import paginate_parameters
from sthali_crud.routers import Base as BaseRouter
from sthali_crud.routers.api import API
from sthali_db import ModelType, SchemaType

from ..templates import Templates


def get_field_form_type(_type: type) -> str:
    """Map Python types to HTML form input types.

    Args:
    ----
        _type: The Python type to map.

    Returns:
    -------
        The corresponding HTML input type.

    """
    origin = get_origin(_type)
    if origin is not None:
        args = get_args(_type)
        # Filter out NoneType from Optional/Union types
        args = [arg for arg in args if arg is not type(None)]
        if args:
            _type = args[0]

    type_mapping = {
        UUID: "text",
        str: "text",
        int: "number",
        float: "number",
        bool: "checkbox",
    }
    return type_mapping.get(_type, "text")


class VIEWS(BaseRouter):
    """HTML view handler for CRUD operations with customizable templates."""

    prefix = "/views"
    templates = Templates().get_templates()

    def __init__(self, db_session, model: ModelType, create_schema: SchemaType, read_schema: SchemaType, update_schema: SchemaType, api: API) -> None:
        """Initialize the VIEWS handler.

        Args:
        ----
            *args: Positional arguments passed to parent BaseRouter class.
            **kwargs: Keyword arguments passed to parent BaseRouter class.

        """
        super().__init__(db_session, model, create_schema, read_schema, update_schema)
        self.api = api

    @property
    def local_context(self) -> dict[str, str]:
        """Base context for current view templates.

        Returns:
        -------
            Dictionary with base context values.

        """
        return {
            "url_for_view_read_many": f"view_read_many_{self.resource_name}",
            "url_for_view_create": f"view_create_{self.resource_name}",
            "url_for_view_read": f"view_read_{self.resource_name}",
        }

    @property
    def api_router(self) -> APIRouter:
        """Create and configure the API router for view endpoints.

        Returns:
        -------
            Configured APIRouter with view routes.

        """
        router = APIRouter(prefix=f"/{self.resource_name}", tags=["views", self.resource_name])
        router.add_api_route(
            "/",
            self.read_many_endpoint,
            name=f"view_read_many_{self.resource_name}",
            response_class=HTMLResponse,
            methods=["GET"],
        )
        router.add_api_route(
            "/new",
            self.create_endpoint,
            name=f"view_create_{self.resource_name}",
            response_class=HTMLResponse,
            methods=["GET"],
        )
        router.add_api_route(
            "/{resource_id}",
            self.read_endpoint,
            name=f"view_read_{self.resource_name}",
            response_class=HTMLResponse,
            methods=["GET"],
        )
        return router

    def _get_table_headers(self, pks: list[str] | None = None) -> list[str]:
        """{...}."""
        model_fields = list(self.read_schema.model_fields.keys())
        for pk in pks or []:
            if pk in model_fields:
                model_fields.remove(pk)
                model_fields.insert(0, pk)
        return model_fields

    def _get_form_fields(
        self, ignored_fields: list[str] | None = None, disabled_fields: list[str] | None = None,
        pks: list[str] | None = None,
    ) -> list[dict[str, str]]:
        """Generate form field metadata for frontend rendering.

        Args:
        ----
            ignored_fields: Fields to exclude from the form.
            disabled_fields: Fields that should be disabled in the form.

        Returns:
        -------
            Dictionary mapping field names to their form metadata.

        """
        ignored_fields = ignored_fields or []
        disabled_fields = disabled_fields or []
        model_fields = []
        for k, v in self.read_schema.model_fields.items():
            if k in ignored_fields:
                continue
            model_fields.append({
                "name": k,
                "type": get_field_form_type(v.annotation),
                "disabled": "disabled" if k in disabled_fields else "",
                "required": "required" if v.is_required() else "",
            })
        for pk in pks or []:
            for field in model_fields:
                if pk in field["name"]:
                    model_fields.remove(field)
                    model_fields.insert(0, field)
        return model_fields

    async def create_endpoint(self, request: Request) -> HTMLResponse:
        """Render the create form view.

        Args:
        ----
            request: The HTTP request object.

        Returns:
        -------
            HTML response with create form template.

        """
        ignored_fields = ["id", "links"]
        pks = ["id"]
        context = {
            **self.local_context,
            **self.api.local_context,
            "form_fields": self._get_form_fields(ignored_fields, pks=pks),
            "form_action": "CREATE",
        }
        return self.templates.TemplateResponse(request, "crud/create.html", context)


    async def read_endpoint(self, request: Request, resource_id: UUID) -> HTMLResponse:
        """Render the read/edit view for a single resource.

        Args:
        ----
            request: The HTTP request object.
            resource_id: The ID of the resource to read.

        Returns:
        -------
            HTML response with read form template.

        """
        result = await self.api.read_endpoint(resource_id)
        ignored_fields = ["links"]
        disabled_fields = ["id"]
        pks = ["id"]
        context = {
            **self.local_context,
            **self.api.local_context,
            "form_fields": self._get_form_fields(ignored_fields, disabled_fields, pks),
            "resource": result,
            "form_action": "UPDATE",
        }
        return self.templates.TemplateResponse(request, "crud/read.html", context)


    async def read_many_endpoint(self, request: Request, paginate_parameters: paginate_parameters = None) -> HTMLResponse:
        """Render the list view for multiple resources.

        Args:
        ----
            request: The HTTP request object.
            paginate_parameters: Pagination parameters for retrieving items.

        Returns:
        -------
            HTML response with list template showing all resources.

        """
        resources = await self.api.read_many_endpoint(paginate_parameters)
        pks = ["id"]
        table_headers = self._get_table_headers(pks)
        context = {
            **self.local_context,
            "resources": resources,
            "table_headers": table_headers,
        }
        return self.templates.TemplateResponse(request, "crud/read_many.html", context)

