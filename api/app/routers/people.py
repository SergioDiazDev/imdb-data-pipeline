from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.models.name import NameBasic
from app.schemas.name import NameBasicOut
from app.db import get_db

router = APIRouter(prefix="/people", tags=["People"])

@router.get("/search", response_model=List[NameBasicOut])
def search_people(
	name: str = Query(..., min_length=1),
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db),
):
	pattern = f"%{name.lower()}%"
	results = (
		db.query(NameBasic)
		.filter(func.lower(NameBasic.primaryName).like(pattern))
		.offset(skip)
		.limit(limit)
		.all()
	)
	return results


@router.get("/{nconst}", response_model=NameBasicOut)
def get_person(nconst: str, db: Session = Depends(get_db)):
	person = db.query(NameBasic).filter(NameBasic.nconst == nconst).first()
	if not person:
		raise HTTPException(status_code=404, detail="Person not found")
	return person

@router.get("/", response_model=List[NameBasicOut])
def list_people(
	nconst: Optional[str] = Query(None),
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db),
):
	if nconst:
		person = db.query(NameBasic).filter(NameBasic.nconst == nconst).first()
		if not person:
			raise HTTPException(status_code=404, detail="Person not found")
		return [person]
	return db.query(NameBasic).offset(skip).limit(limit).all()
