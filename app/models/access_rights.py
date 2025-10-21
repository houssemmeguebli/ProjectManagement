from sqlalchemy import Column, Integer, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship, validates
from enum import Enum as PyEnum
from ..db.database import Base

class AccessRole(PyEnum):
    OWNER = "owner"
    CONTRIBUTOR = "contributor"
    VISITOR = "visitor"

class ProjectAccess(Base):
    __tablename__ = "project_access"
    __table_args__ = (
        CheckConstraint('user_id > 0', name='access_user_id_positive'),
        CheckConstraint('project_id > 0', name='access_project_id_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(Enum(AccessRole), nullable=False)

    user = relationship("User")
    project = relationship("Project")
    
    @validates('user_id')
    def validate_user_id(self, key, user_id):
        if user_id <= 0:
            raise ValueError('User ID must be a positive integer')
        return user_id
    
    @validates('project_id')
    def validate_project_id(self, key, project_id):
        if project_id <= 0:
            raise ValueError('Project ID must be a positive integer')
        return project_id
    
    @validates('role')
    def validate_role(self, key, role):
        if role not in AccessRole:
            raise ValueError(f'Role must be one of: {[r.value for r in AccessRole]}')
        return role