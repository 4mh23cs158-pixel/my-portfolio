from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectResponse


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


# ==========================================
# ADMIN AUTHENTICATION CHECK
# ==========================================

def require_admin(request: Request):

    if not request.session.get("admin"):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return True


# ==========================================
# GET ALL PROJECTS
# PUBLIC
# ==========================================

@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):

    projects = db.query(Project).all()

    return projects


# ==========================================
# GET ONE PROJECT
# PUBLIC
# ==========================================

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


# ==========================================
# CREATE PROJECT
# ADMIN ONLY
# ==========================================

@router.post("/", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    project = Project(
        title=project_data.title,
        description=project_data.description,
        technologies=project_data.technologies,
        github_url=project_data.github_url,
        deployed_url=project_data.deployed_url,
        image_url=project_data.image_url
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# ==========================================
# UPDATE PROJECT
# ADMIN ONLY
# ==========================================

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project.title = project_data.title
    project.description = project_data.description
    project.technologies = project_data.technologies
    project.github_url = project_data.github_url
    project.deployed_url = project_data.deployed_url
    project.image_url = project_data.image_url

    db.commit()
    db.refresh(project)

    return project


# ==========================================
# DELETE PROJECT
# ADMIN ONLY
# ==========================================

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }