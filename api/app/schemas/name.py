from pydantic import BaseModel
from typing import Optional

class NameBasic(BaseModel):
	nconst: str
	primaryName: Optional[str] = None
	birthYear: Optional[int] = None
	deathYear: Optional[int] = None
	primaryProfession: Optional[str] = None
	knownForTitles: Optional[str] = None

class NameBasicOut(NameBasic):
	class Config:
		from_attributes = True