from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey
from .base import Base

class TitleAkas(Base):
	__tablename__ = "title_akas"

	titleId: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	title: Mapped[str]
	region: Mapped[str]
	language: Mapped[str]
	types: Mapped[str]
	attributes: Mapped[str]
	isOriginalTitle: Mapped[bool]

	# Relación corregida (eliminada redundancia)
	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="akas")