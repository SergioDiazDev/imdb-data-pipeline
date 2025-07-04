from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey
from .base import Base

class TitlePrincipal(Base):
	__tablename__ = "title_principals"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	ordering: Mapped[int]
	nconst: Mapped[str] = mapped_column(ForeignKey("name_basics.nconst"))
	category: Mapped[str]
	job: Mapped[Optional[str]]
	characters: Mapped[Optional[str]]

	# Relaciones corregidas
	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="principals")
	person: Mapped["NameBasic"] = relationship("NameBasic", back_populates="principals")