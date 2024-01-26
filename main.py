from datetime import timedelta
#from winreg import HKEY_CURRENT_USER
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from db import SessionLocal, engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tokens import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token, verify_password
import models
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from tokens import SECRET_KEY, ALGORITHM, TokenData
from fastapi.security import OAuth2PasswordBearer

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user.username


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.create_book(db=db, book=book)

@app.get("/books", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{isbn}", response_model=schemas.Book)
def read_book(isbn: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_book = crud.get_book_by_isbn(db, isbn=isbn)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{isbn}", response_model=schemas.Book)
def update_book(isbn: str, book: schemas.BookCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_book = crud.update_book(db, isbn=isbn, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{isbn}", response_model=schemas.Book)
def delete_book(isbn: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_book = crud.delete_book(db, isbn=isbn)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book




# Replace this with your actual user fetching logic
def get_user(db: Session, username: str) -> models.User:
    """
    Fetch a user by username from the database.

    :param db: Database session.
    :param username: Username of the user to fetch.
    :return: User object if found, otherwise None.
    """
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except Exception as e:
        # Handle or log the exception as appropriate
        return None



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/protected-route/")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You have accessed a protected route."}



#jwt auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Add your authentication function here
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

