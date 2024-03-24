from sqlalchemy.orm import Session, selectinload

from . import models, schemas


def get_user(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )


def get_users_by_telegram_id(db: Session, telegram_id: int):
    return (
        db.query(models.User)
        .filter(models.User.telegram_id == telegram_id)
        .all()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(
        selectinload(models.User.cigarettes)
    ).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(telegram_id=user.telegram_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_cigarettes(db: Session, user_id: int, limit: int = 2):
    return (
        db.query(models.Cigarette)
        .filter(models.Cigarette.smoker_id == user_id)
        .order_by(models.Cigarette.smoking_time.desc())
        .limit(limit)
        .all()
    )


def add_user_cigarette(db: Session, cigarette: schemas.CigaretteCreate,
                       user_id: int):
    db_cigarette = models.Cigarette(
        **cigarette.model_dump(),
        smoker_id=user_id
    )
    db.add(db_cigarette)
    db.commit()
    db.refresh(db_cigarette)
    return db_cigarette
