from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=False)

    technologies = Column(String(500), nullable=False)

    github_url = Column(String(500), nullable=True)

    deployed_url = Column(String(500), nullable=True)

    image_url = Column(String(500), nullable=True)