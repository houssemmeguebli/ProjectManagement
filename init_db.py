#!/usr/bin/env python3
"""
Database initialization script
Creates tables and optionally adds sample data
"""

from app.db.database import engine, Base
from app.models import User, Project, Task, Comment

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()