from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, List

class Base(DeclarativeBase):
	pass

class NameBasic(Base):
	__tablename__ = "name_basics"

	nconst: Mapped[str] = mapped_column(primary_key=True)
	primaryName: Mapped[Optional[str]]
	birthYear: Mapped[Optional[int]]
	deathYear: Mapped[Optional[int]]
	primaryProfession: Mapped[Optional[str]]
	knownForTitles: Mapped[Optional[str]]

	principals: Mapped[List["TitlePrincipal"]] = relationship("TitlePrincipal", back_populates="person")

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

	akas: Mapped[List["TitleAkas"]] = relationship("TitleAkas", back_populates="title_basic")
	crew: Mapped[Optional["TitleCrew"]] = relationship("TitleCrew", back_populates="title_basic", uselist=False)
	episode: Mapped[Optional["TitleEpisode"]] = relationship(
		"TitleEpisode",
		back_populates="title_basic",
		uselist=False,
		foreign_keys="[TitleEpisode.tconst]"  # Necesario para evitar ambigüedad (ver abajo)
	)
	episodes_as_parent: Mapped[List["TitleEpisode"]] = relationship(  # Para el parentTconst
		"TitleEpisode",
		back_populates="parent_title",
		foreign_keys="[TitleEpisode.parentTconst]"
	)
	principals: Mapped[List["TitlePrincipal"]] = relationship("TitlePrincipal", back_populates="title_basic")
	rating: Mapped[Optional["TitleRating"]] = relationship("TitleRating", back_populates="title_basic", uselist=False)

class TitleAkas(Base):
	__tablename__ = "title_akas"

	titleId: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	ordering: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	region: Mapped[Optional[str]]
	language: Mapped[Optional[str]]
	types: Mapped[Optional[str]]
	attributes: Mapped[Optional[str]]
	isOriginalTitle: Mapped[Optional[bool]]

	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="akas")

class TitleCrew(Base):
	__tablename__ = "title_crew"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	directors: Mapped[Optional[str]]
	writers: Mapped[Optional[str]]

	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="crew")

class TitleEpisode(Base):
	__tablename__ = "title_episode"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	parentTconst: Mapped[Optional[str]] = mapped_column(ForeignKey("title_basics.tconst"))
	seasonNumber: Mapped[Optional[int]]
	episodeNumber: Mapped[Optional[int]]

	title_basic: Mapped["TitleBasic"] = relationship(
		"TitleBasic",
		back_populates="episode",
		foreign_keys=[tconst]
	)
	parent_title: Mapped[Optional["TitleBasic"]] = relationship(
		"TitleBasic",
		back_populates="episodes_as_parent",
		foreign_keys=[parentTconst]
	)

class TitlePrincipal(Base):
	__tablename__ = "title_principals"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	ordering: Mapped[int] = mapped_column(primary_key=True)
	nconst: Mapped[str] = mapped_column(ForeignKey("name_basics.nconst"))
	category: Mapped[Optional[str]]
	job: Mapped[Optional[str]]
	characters: Mapped[Optional[str]]

	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="principals")
	person: Mapped["NameBasic"] = relationship("NameBasic", back_populates="principals")

class TitleRating(Base):
	__tablename__ = "title_ratings"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	averageRating: Mapped[float]
	numVotes: Mapped[int]

	title_basic: Mapped["TitleBasic"] = relationship("TitleBasic", back_populates="rating")
