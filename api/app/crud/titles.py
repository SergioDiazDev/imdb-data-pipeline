from sqlalchemy.orm import Session
from sqlalchemy import func, nullslast
from app.models.title import TitleBasic

def get_title(db: Session, tconst: str):
	return (
		db.query(TitleBasic)
		.filter(TitleBasic.tconst == tconst)
		.first()
	)

def get_titles(db: Session, skip: int = 0, limit: int = 100):
	return (
		db.query(TitleBasic)
		.order_by(TitleBasic.tconst)  # Añadido orden determinista
		.offset(skip)
		.limit(limit)
		.all()
	)

def search_titles_by_original_title(db: Session, original_title: str, skip: int = 0, limit: int = 100):
	pattern = f"%{original_title.lower()}%"
	return (
		db.query(TitleBasic)
		.filter(func.lower(TitleBasic.originalTitle).ilike(pattern))  # ilike para case-insensitive
		.order_by(nullslast(TitleBasic.originalTitle), TitleBasic.tconst, TitleBasic.startYear)  # Orden total y estable
		.offset(skip)
		.limit(limit)
		.all()
	)
