from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey
from .base import Base

class TitleRating(Base):
	__tablename__ = "title_ratings"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	averageRating: Mapped[Optional[float]]
	numVotes: Mapped[Optional[int]]

	# Relación corregida
	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="rating")