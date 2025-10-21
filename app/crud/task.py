from sqlalchemy.orm import Session
from typing import List
from ..models.task import Task, TaskStatus
from ..schemas.task import TaskCreate, TaskUpdate

class TaskCRUD:
    def create(self, db: Session, task_create: TaskCreate) -> Task:
        db_task = Task(**task_create.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get_by_id(self, db: Session, task_id: int) -> Task:
        return db.query(Task).filter(Task.id == task_id).first()

    def get_by_project(self, db: Session, project_id: int) -> List[Task]:
        return db.query(Task).filter(Task.project_id == project_id).all()

    def get_by_user(self, db: Session, user_id: int) -> List[Task]:
        return db.query(Task).filter(Task.assigned_user_id == user_id).all()

    def get_by_status(self, db: Session, status: TaskStatus) -> List[Task]:
        return db.query(Task).filter(Task.status == status).all()

    def update(self, db: Session, task: Task, task_update: TaskUpdate) -> Task:
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, task: Task):
        db.delete(task)
        db.commit()

task_crud = TaskCRUD()