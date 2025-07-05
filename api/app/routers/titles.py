from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, nullslast
from typing import List, Optional

from app.models.title import TitleBasic
from app.schemas.title import TitleOut
from app.db import get_db

router = APIRouter(prefix="/titles", tags=["Titles"])

@router.get("/search", response_model=List[TitleOut])
def search_titles_by_original_title(
	originalTitle: str = Query(..., min_length=1),
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db)
):
	pattern = f"%{originalTitle.lower()}%"
	results = (
		db.query(TitleBasic)
		.filter(func.lower(TitleBasic.originalTitle).like(pattern))
		.order_by(TitleBasic.originalTitle, TitleBasic.tconst)  # Orden total y estable
		.offset(skip)
		.limit(limit)
		.all()
	)
	return results

@router.get("/{tconst}", response_model=TitleOut)
def read_title_path(tconst: str, db: Session = Depends(get_db)):
	title = db.query(TitleBasic).filter(TitleBasic.tconst == tconst).first()
	if not title:
		raise HTTPException(status_code=404, detail="Title not found")
	return title

@router.get("/", response_model=List[TitleOut])
def read_titles(
	tconst: Optional[str] = Query(None),
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db)
):
	if tconst:
		title = db.query(TitleBasic).filter(TitleBasic.tconst == tconst).first()
		if title:
			return [title]
		raise HTTPException(status_code=404, detail="Title not found")
	return db.query(TitleBasic).offset(skip).limit(limit).all()