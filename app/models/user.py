from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, validates
from ..db.database import Base
import re

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint('length(username) >= 3 AND length(username) <= 50', name='username_length'),
        CheckConstraint('length(email) >= 5 AND length(email) <= 100', name='email_length'),
        CheckConstraint('length(hashed_password) > 0', name='password_not_empty'),
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    contributed_projects = relationship("Project", secondary="project_contributors", back_populates="contributors")
    
    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username.strip()) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(username) > 50:
            raise ValueError('Username cannot exceed 50 characters')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return username.strip()
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or len(email.strip()) < 5:
            raise ValueError('Email must be at least 5 characters long')
        if len(email) > 100:
            raise ValueError('Email cannot exceed 100 characters')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')
        return email.strip().lower()