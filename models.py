from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db_helper import db


class Expenses(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
