from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from .database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())

    cigarettes = relationship(
        "Cigarette",
        back_populates="smoker",
        order_by="Cigarette.smoking_time.desc()",
    )


class Cigarette(Base):
    __tablename__ = 'cigarettes'

    id: Mapped[intpk]
    smoker_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    smoking_time: Mapped[datetime]

    smoker = relationship("User", back_populates="cigarettes")
