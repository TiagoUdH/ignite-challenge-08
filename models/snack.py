import datetime
from database import db
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

class Snack(db.Model):
  __tablename__ = "snacks"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30), nullable=False)
  description: Mapped[str] = mapped_column(String(120), nullable=False)
  created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
  in_diet: Mapped[bool] = mapped_column(Boolean, default=False)