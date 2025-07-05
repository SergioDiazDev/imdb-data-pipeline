from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import ForeignKey
from .base import Base

class TitleBasic(Base):
	__tablename__ = "title_basics"

	tconst: Mapped[str] = mapped_column(primary_key=True)
	titleType: Mapped[str]
	primaryTitle: Mapped[str]
	originalTitle: Mapped[str]
	isAdult: Mapped[float]
	startYear: Mapped[Optional[float]]
	endYear: Mapped[Optional[float]]
	runtimeMinutes: Mapped[Optional[float]]
	genres: Mapped[Optional[str]]

	