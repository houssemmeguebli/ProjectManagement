from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from ..db.database import Base

class AccessRole(PyEnum):
    OWNER = "owner"
    CONTRIBUTOR = "contributor"
    VISITOR = "visitor"

class ProjectAccess(Base):
    __tablename__ = "project_access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(Enum(AccessRole), nullable=False)

    user = relationship("User")
    project = relationship("Project")