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

	# Relaciones corregidas y simplificadas
	akas: Mapped[List["TitleAkas"]] = relationship("TitleAkas", back_populates="title_basic")
	crew: Mapped[List["TitleCrew"]] = relationship("TitleCrew", back_populates="title_basic")
	episode: Mapped[Optional["TitleEpisode"]] = relationship(
		"TitleEpisode",
		back_populates="title_basic",
		foreign_keys="[TitleEpisode.tconst]"
	)
	episodes_as_parent: Mapped[List["TitleEpisode"]] = relationship(
		"TitleEpisode",
		back_populates="parent_title",
		foreign_keys="[TitleEpisode.parentTconst]"
	)
	principals: Mapped[List["TitlePrincipal"]] = relationship("TitlePrincipal", back_populates="title_basic")
	rating: Mapped[Optional["TitleRating"]] = relationship("TitleRating", back_populates="title_basic")