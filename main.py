from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import timedelta

from database import get_db, engine
from models import Base, User, Category, Question
from schemas import (
    UserCreate, User as UserSchema,
    CategoryCreate, Category as CategorySchema,
    QuestionCreate, Question as QuestionSchema,
    Token
)
from auth import (
    get_password_hash, verify_password,
    create_access_token, get_current_user,
    get_current_active_admin
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {
        "title": "Quiz API",
        "description": "A FastAPI-based quiz application",
        "documentation": "/docs",
        "redoc_documentation": "/redoc",
        "version": "1.0.0",
        "status": "running"
    }

# Authentication routes
@app.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Category routes
@app.post("/categories/", response_model=CategorySchema)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

# Question routes
@app.post("/questions/", response_model=QuestionSchema)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.get("/questions/", response_model=List[QuestionSchema])
def read_questions(
    category_id: int = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if category_id:
        query = query.filter(Question.category_id == category_id)
    questions = query.offset(skip).limit(limit).all()
    return questions

@app.get("/questions/{question_id}", response_model=QuestionSchema)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
