from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship, validates
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
    __table_args__ = (
        CheckConstraint('length(title) >= 1 AND length(title) <= 200', name='title_length'),
        CheckConstraint('description IS NULL OR length(description) <= 2000', name='description_length'),
        CheckConstraint('owner_id > 0', name='owner_id_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    description = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", foreign_keys=[owner_id])
    contributors = relationship("User", secondary=project_contributors, back_populates="contributed_projects")
    tasks = relationship("Task", back_populates="project")
    access_rights = relationship("ProjectAccess", back_populates="project")
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Project title cannot be empty')
        if len(title) > 200:
            raise ValueError('Project title cannot exceed 200 characters')
        return title.strip()
    
    @validates('description')
    def validate_description(self, key, description):
        if description and len(description) > 2000:
            raise ValueError('Project description cannot exceed 2000 characters')
        return description.strip() if description else description
    
    @validates('owner_id')
    def validate_owner_id(self, key, owner_id):
        if owner_id <= 0:
            raise ValueError('Owner ID must be a positive integer')
        return owner_id