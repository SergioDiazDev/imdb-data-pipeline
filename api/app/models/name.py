from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import ForeignKey
from .base import Base

class NameBasic(Base):
	__tablename__ = "name_basics"

	nconst: Mapped[str] = mapped_column(primary_key=True)
	primaryName: Mapped[Optional[str]]
	birthYear: Mapped[Optional[int]]
	deathYear: Mapped[Optional[int]]
	primaryProfession: Mapped[Optional[str]]
	knownForTitles: Mapped[Optional[str]]

	# Relación corregida (eliminada redundancia)
	principals: Mapped[List["TitlePrincipal"]] = relationship("TitlePrincipal", back_populates="person")