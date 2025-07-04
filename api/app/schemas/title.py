from pydantic import BaseModel
from typing import Optional

class TitleBase(BaseModel):
	tconst: str
	titleType: str
	primaryTitle: str
	originalTitle: str
	isAdult: float
	startYear: Optional[float] = None
	endYear: Optional[float] = None
	runtimeMinutes: Optional[float] = None
	genres: Optional[str] = None

class TitleOut(TitleBase):
	class Config:
		from_attributes = True