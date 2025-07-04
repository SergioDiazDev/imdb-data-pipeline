from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey
from .base import Base

class TitleCrew(Base):
	__tablename__ = "title_crew"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	nconst: Mapped[str] = mapped_column(ForeignKey("name_basics.nconst"), primary_key=True)
	job: Mapped[str]
	department: Mapped[str]

	# Relaciones corregidas
	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="crew")