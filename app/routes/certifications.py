from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Certification
from app.schemas import (
    CertificationCreate,
    CertificationResponse
)


router = APIRouter(
    prefix="/api/certifications",
    tags=["Certifications"]
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
# GET ALL CERTIFICATIONS
# PUBLIC
# ==========================================

@router.get(
    "/",
    response_model=list[CertificationResponse]
)
def get_certifications(
    db: Session = Depends(get_db)
):

    certifications = db.query(
        Certification
    ).all()

    return certifications


# ==========================================
# GET ONE CERTIFICATION
# PUBLIC
# ==========================================

@router.get(
    "/{certification_id}",
    response_model=CertificationResponse
)
def get_certification(
    certification_id: int,
    db: Session = Depends(get_db)
):

    certification = db.query(
        Certification
    ).filter(
        Certification.id == certification_id
    ).first()

    if not certification:

        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    return certification


# ==========================================
# CREATE CERTIFICATION
# ADMIN ONLY
# ==========================================

@router.post(
    "/",
    response_model=CertificationResponse
)
def create_certification(
    certification_data: CertificationCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    certification = Certification(
        title=certification_data.title,
        organization=certification_data.organization,
        issue_date=certification_data.issue_date,
        certificate_url=certification_data.certificate_url,
        image_url=certification_data.image_url
    )

    db.add(certification)
    db.commit()
    db.refresh(certification)

    return certification


# ==========================================
# UPDATE CERTIFICATION
# ADMIN ONLY
# ==========================================

@router.put(
    "/{certification_id}",
    response_model=CertificationResponse
)
def update_certification(
    certification_id: int,
    certification_data: CertificationCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    certification = db.query(
        Certification
    ).filter(
        Certification.id == certification_id
    ).first()

    if not certification:

        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    certification.title = certification_data.title

    certification.organization = (
        certification_data.organization
    )

    certification.issue_date = (
        certification_data.issue_date
    )

    certification.certificate_url = (
        certification_data.certificate_url
    )

    certification.image_url = (
        certification_data.image_url
    )

    db.commit()
    db.refresh(certification)

    return certification


# ==========================================
# DELETE CERTIFICATION
# ADMIN ONLY
# ==========================================

@router.delete(
    "/{certification_id}"
)
def delete_certification(
    certification_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin)
):

    certification = db.query(
        Certification
    ).filter(
        Certification.id == certification_id
    ).first()

    if not certification:

        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    db.delete(certification)
    db.commit()

    return {
        "message": "Certification deleted successfully"
    }