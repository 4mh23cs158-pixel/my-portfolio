from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

   
    technologies = Column(String(500), nullable=False)

    github_url = Column(String(500), nullable=True)

    deployed_url = Column(String(500), nullable=True)

    image_url = Column(String(500), nullable=True)


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    organization = Column(String(200), nullable=False)

    issue_date = Column(String(100), nullable=True)

    certificate_url = Column(String(500), nullable=True)

    image_url = Column(String(500), nullable=True)