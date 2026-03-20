"""Pydantic schemas for API request/response models.

This module provides base schemas with form field generation and HATEOAS support.
"""
from datetime import date
from uuid import UUID

from sthali_db import BaseSchema


class ProjectCreateSchema(BaseSchema):
    class Config:
        title = "Project"

    name: str
    description: str
    category: str = "General"
    is_active: bool = True
    priority_level: int = 1
    budget: int = 0
    start_date: date
    end_date: date
    new_name: str
    new_description: str
    new_category: str = "General"
    new_is_active: bool = True
    new_priority_level: int = 1
    new_budget: int = 0
    new_start_date: date
    new_end_date: date


class ProjectUpdateSchema(ProjectCreateSchema):
    pass

class ProjectReadSchema(ProjectCreateSchema):
    """Schema for reading Project data with ID."""

    id: UUID


ProjectSchemas = (ProjectCreateSchema, ProjectReadSchema, ProjectUpdateSchema)