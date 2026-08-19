from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================
# PROJECT SCHEMAS
# ==========================================

class ProjectCreate(BaseModel):

    title: str

    description: str

    technologies: str

    github_url: Optional[str] = None

    deployed_url: Optional[str] = None

    image_url: Optional[str] = None


class ProjectResponse(ProjectCreate):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# CERTIFICATION SCHEMAS
# ==========================================

class CertificationCreate(BaseModel):

    title: str

    organization: str

    issue_date: Optional[str] = None

    certificate_url: Optional[str] = None

    image_url: Optional[str] = None


class CertificationResponse(CertificationCreate):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )