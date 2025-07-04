from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey
from .base import Base

class TitleEpisode(Base):
	__tablename__ = "title_episodes"

	tconst: Mapped[str] = mapped_column(ForeignKey("title_basics.tconst"), primary_key=True)
	parentTconst: Mapped[Optional[str]] = mapped_column(ForeignKey("title_basics.tconst"))
	seasonNumber: Mapped[Optional[int]]
	episodeNumber: Mapped[Optional[int]]

	# Relaciones corregidas
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