"""{...}."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..templates import Templates


class ROOT:
    """{...}."""
    templates = Templates().get_templates()

    @property
    def api_router(self) -> APIRouter:
        router = APIRouter(tags=["views", "root"])
        router.add_api_route(
            "/",
            self.root,
            response_class=HTMLResponse,
            methods=["GET"],
        )
        return router

    def root(self, request: Request):
        return self.templates.TemplateResponse(request, "index.html")
