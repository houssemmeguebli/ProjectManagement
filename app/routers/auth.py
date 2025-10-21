from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models import User
from ..schemas.user import UserCreate, UserResponse, UserLogin
from ..schemas.token import Token
from ..crud.user import user_crud
from ..core.security import verify_password, create_access_token, verify_token
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
user_router = APIRouter(tags=["users"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = user_crud.get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/signup",
    response_model=UserResponse,
    summary="Register a new user",
    description="Create a new user account with username, email, and password",
    responses={
        200: {"description": "User created successfully"},
        400: {"description": "Username already exists"}
    }
)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_by_username(db, user_create.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if user_crud.get_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create(db, user_create)

@router.post("/login",
    response_model=Token,
    summary="Login user",
    description="Authenticate user and return JWT access token",
    responses={
        200: {"description": "Login successful, returns access token"},
        401: {"description": "Invalid username or password"}
    }
)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_by_email(db, user_login.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/users/{user_id}", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user