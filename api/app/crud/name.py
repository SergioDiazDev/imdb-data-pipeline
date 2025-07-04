# app/crud/name.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.name import NameBasic

def get_person(db: Session, nconst: str) -> Optional[NameBasic]:
	return db.query(NameBasic).filter(NameBasic.nconst == nconst).first()

def get_people(db: Session, skip: int = 0, limit: int = 100) -> List[NameBasic]:
	return db.query(NameBasic).offset(skip).limit(limit).all()

def search_people_by_name(db: Session, name: str, skip: int = 0, limit: int = 100) -> List[NameBasic]:
	pattern = f"%{name.lower()}%"
	return (
		db.query(NameBasic)
		.filter(NameBasic.primaryName.ilike(pattern))
		.offset(skip)
		.limit(limit)
		.order_by(NameBasic.primaryName)
		.all()
	)
