from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProjectCreate(BaseModel):
    title: str
    description: str
    technologies: str
    github_url: Optional[str] = None
    deployed_url: Optional[str] = None
    image_url: Optional[str] = None


class ProjectResponse(ProjectCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)