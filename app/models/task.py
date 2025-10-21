from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, validates
from enum import Enum as PyEnum
from datetime import datetime
from ..db.database import Base

class TaskStatus(PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint('length(title) >= 1 AND length(title) <= 200', name='task_title_length'),
        CheckConstraint('description IS NULL OR length(description) <= 1000', name='task_description_length'),
        CheckConstraint('project_id > 0', name='task_project_id_positive'),
        CheckConstraint('assigned_user_id IS NULL OR assigned_user_id > 0', name='task_assigned_user_id_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    description = Column(String(1000))
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User")
    comments = relationship("Comment", back_populates="task")
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Task title cannot be empty')
        if len(title) > 200:
            raise ValueError('Task title cannot exceed 200 characters')
        return title.strip()
    
    @validates('description')
    def validate_description(self, key, description):
        if description and len(description) > 1000:
            raise ValueError('Task description cannot exceed 1000 characters')
        return description.strip() if description else description
    
    @validates('project_id')
    def validate_project_id(self, key, project_id):
        if project_id <= 0:
            raise ValueError('Project ID must be a positive integer')
        return project_id
    
    @validates('assigned_user_id')
    def validate_assigned_user_id(self, key, assigned_user_id):
        if assigned_user_id is not None and assigned_user_id <= 0:
            raise ValueError('Assigned user ID must be a positive integer')
        return assigned_user_id