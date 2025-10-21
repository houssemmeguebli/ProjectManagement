from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from ..db.database import Base

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = (
        CheckConstraint('length(text) >= 1 AND length(text) <= 1000', name='comment_text_length'),
        CheckConstraint('author_id > 0', name='comment_author_id_positive'),
        CheckConstraint('task_id > 0', name='comment_task_id_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship("User")
    task = relationship("Task", back_populates="comments")
    
    @validates('text')
    def validate_text(self, key, text):
        if not text or len(text.strip()) == 0:
            raise ValueError('Comment text cannot be empty')
        if len(text) > 1000:
            raise ValueError('Comment text cannot exceed 1000 characters')
        return text.strip()
    
    @validates('author_id')
    def validate_author_id(self, key, author_id):
        if author_id <= 0:
            raise ValueError('Author ID must be a positive integer')
        return author_id
    
    @validates('task_id')
    def validate_task_id(self, key, task_id):
        if task_id <= 0:
            raise ValueError('Task ID must be a positive integer')
        return task_id