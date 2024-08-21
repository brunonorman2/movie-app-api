from sqlalchemy.orm import Session
import models as models
import schema as schema
from logger import get_logger

logger = get_logger(__name__)

def create_user(db: Session, user: schema.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_movie(db: Session, id: int):
    logger.info('Querying Movie model')
    return db.query(models.Movie).filter(models.Movie.id == id).first()

def get_movie_by_producer(db: Session, producer: str):
    return db.query(models.Movie).filter(models.Movie.producer == producer).first()

def get_movies(db: Session, user_id: int = None, offset: int = 0, limit: int = 10):
    return db.query(models.Movie).filter(models.Movie.user_id == user_id).offset(offset).limit(limit).all()

def create_movie(db: Session, movie: schema.MovieCreate, user_id: int = None):
    db_book = models.Movie(
        **movie.model_dump(),
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, book_payload: schema.MovieUpdate):
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    
    movie_payload_dict = movie_payload.dict(exclude_unset=True)

    for k, v in movie_payload_dict.items():
        setattr(movie, k, v)


    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie

def delete_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
        return True
    return False