from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from ..db.database import Base

project_contributors = Table(
    'project_contributors',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", foreign_keys=[owner_id])
    contributors = relationship("User", secondary=project_contributors, back_populates="contributed_projects")
    tasks = relationship("Task", back_populates="project")
    access_rights = relationship("ProjectAccess", back_populates="project")