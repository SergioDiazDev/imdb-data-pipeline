from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import TitleBasic
from app.db import get_db

router = APIRouter(prefix="/titles", tags=["Titles"])

@router.get("/{tconst}")
def get_title(tconst: str, db: Session = Depends(get_db)):
	title = db.query(TitleBasic).filter(TitleBasic.tconst == tconst).first()
	if not title:
		raise HTTPException(status_code=404, detail="Title not found")
	return title
