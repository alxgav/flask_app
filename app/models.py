from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float]
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="expenses")

    def __repr__(self):
        return f"Expenses(title={self.title}, amount={self.amount})"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]
    expenses: Mapped[list[Expense]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(username={self.username})"
