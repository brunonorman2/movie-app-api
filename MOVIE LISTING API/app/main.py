from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_user
import crud as crud, schema as schema
from database import engine, Base, get_db
from auth import pwd_context
from typing import Optional

from logger import get_logger

logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.post("/signup", response_model=schema.User)
def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    logger.info('Creating user...')
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        logger.warning(f"User with {user.username} already exists.")
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info('User successfully created.')
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    logger.info("Generating authentication token...")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"Token generated for {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/movies/")
def get_movies(
    db: Session = Depends(get_db),
    user: schema.User = Depends(get_current_user),
    offset: int = 0,
    limit: int = 10,
):
    logger.info(f'Getting movies for {user.username} ...')
    movies = crud.get_movies(db, user_id=user.id, offset=offset, limit=limit)
    logger.info(f'Movies gotten for {user.username} successfully.')
    return {"message": "success", "data": movies}


@app.get("/movie/{movie_id}", response_model=schema.Movie)
def get_movie(movie_id: str, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies")
def create_movie(
    payload: schema.MovieCreate,
    user: schema.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    movie = crud.create_movie(db, payload, user_id=user.id)
    return {"message": "success", "data": movie}


@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int, payload: schema.MovieUpdate, db: Session = Depends(get_db)
):
    movie = crud.update_movie(db, movie_id, payload)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "success", "data": movie}


