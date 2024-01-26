from sqlalchemy.orm import Session
import models, schemas
from tokens import get_password_hash

def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, isbn: str, book: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
    if db_book:
        update_data = book.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def delete_book(db: Session, isbn: str):
    db_book = db.query(models.Book).filter(models.Book.isbn == isbn).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



