from sqlalchemy.orm import Session
from typing import List
from ..models.comment import Comment
from ..schemas.comment import CommentCreate

class CommentCRUD:
    def create(self, db: Session, comment_create: CommentCreate, author_id: int) -> Comment:
        comment_data = comment_create.model_dump()
        db_comment = Comment(**comment_data, author_id=author_id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def get_by_task(self, db: Session, task_id: int) -> List[Comment]:
        return db.query(Comment).filter(Comment.task_id == task_id).all()

comment_crud = CommentCRUD()