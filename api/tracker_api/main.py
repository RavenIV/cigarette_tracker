from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserDetail)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_users = crud.get_users_by_telegram_id(db, telegram_id=user.telegram_id)
    if db_users:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.UserList])
def read_users(telegram_id: Union[int, None] = None, limit: int = 100,
               db: Session = Depends(get_db)):
    if telegram_id:
        return crud.get_users_by_telegram_id(db, telegram_id)
    return crud.get_users(db, limit=limit)


def get_user_or_404(user_id: int, db: Session):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}/", response_model=schemas.UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


@app.post("/users/{user_id}/cigarettes/", response_model=schemas.Cigarette)
def add_user_cigarette(user_id: int, cigarette: schemas.CigaretteCreate,
                       db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    return crud.add_user_cigarette(db, cigarette, user.id)


@app.get("/users/{user_id}/cigarettes/",
         response_model=list[schemas.Cigarette])
def read_user_cigarettes(user_id: int, db: Session = Depends(get_db),
                         limit: int = 2):
    user = get_user_or_404(user_id, db)
    return crud.get_user_cigarettes(db, user.id, limit)
