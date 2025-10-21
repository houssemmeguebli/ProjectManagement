from sqlalchemy.orm import Session
from typing import List
from ..models.project import Project
from ..models.user import User
from ..schemas.project import ProjectCreate, ProjectUpdate

class ProjectCRUD:
    def create(self, db: Session, project_create: ProjectCreate, owner_id: int) -> Project:
        db_project = Project(**project_create.model_dump(), owner_id=owner_id)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    def get_by_id(self, db: Session, project_id: int) -> Project:
        return db.query(Project).filter(Project.id == project_id).first()

    def get_user_projects(self, db: Session, user_id: int) -> List[Project]:
        return db.query(Project).filter(
            (Project.owner_id == user_id) | 
            (Project.contributors.any(User.id == user_id))
        ).all()

    def get_projects_by_user_id(self, db: Session, user_id: int) -> List[Project]:
        return db.query(Project).filter(
            (Project.owner_id == user_id) | 
            (Project.contributors.any(User.id == user_id))
        ).all()

    def update(self, db: Session, project: Project, project_update: ProjectUpdate) -> Project:
        for field, value in project_update.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        return project

    def add_contributor(self, db: Session, project: Project, user: User):
        if user not in project.contributors:
            project.contributors.append(user)
            db.commit()
    
    def delete(self, db: Session, project: Project):
        db.delete(project)
        db.commit()

project_crud = ProjectCRUD()