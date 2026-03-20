"""{...}."""

from sqlalchemy import UUID, Boolean, Column, Date, Integer, String
from sthali_db import BaseModel


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    id = Column(UUID, primary_key=True)
    # created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    name = Column(String)
    description = Column(String)
    category = Column(String, default="General")
    is_active = Column(Boolean, default=True)
    priority_level = Column(Integer, default=1)
    budget = Column(Integer, default=0)
    start_date = Column(Date)
    end_date = Column(Date)
    new_name = Column(String)
    new_description = Column(String)
    new_category = Column(String, default="General")
    new_is_active = Column(Boolean, default=True)
    new_priority_level = Column(Integer, default=1)
    new_budget = Column(Integer, default=0)
    new_start_date = Column(Date)
    new_end_date = Column(Date)
