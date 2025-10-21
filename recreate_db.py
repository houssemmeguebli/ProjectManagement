#!/usr/bin/env python3
"""
Database Recreation Script
Drops existing tables and recreates them with updated schema and constraints
"""

import os
from app.db.database import engine, Base
from app.models import User, Project, Task, Comment, ProjectAccess

def recreate_database():
    """Drop all tables and recreate with updated schema and validation constraints"""
    
    # Drop all existing tables first
    Base.metadata.drop_all(bind=engine)
    print("Dropped all existing tables")
    
    # Create all tables with updated schema and constraints
    Base.metadata.create_all(bind=engine)
    print("Created all tables with updated schema and validation constraints")
    
    print("\nTables created with validation:")
    print("- users (username 3-50 chars, email validation)")
    print("- projects (title 1-200 chars, description max 2000)")
    print("- tasks (title 1-200 chars, description max 1000)")
    print("- comments (text 1-1000 chars)")
    print("- project_access (role validation)")
    print("- project_contributors")

if __name__ == "__main__":
    print("Recreating database with validation constraints...")
    recreate_database()
    print("Database recreation completed!")