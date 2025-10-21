from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import auth, projects, tasks, comments

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management API",
    description="A collaborative project management platform built with FastAPI.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(auth.user_router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Project Management API", "docs": "/docs"}
