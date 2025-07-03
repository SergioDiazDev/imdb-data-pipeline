from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import TitleBasic
from app.db import get_db

router = APIRouter(prefix="/titles", tags=["Titles"])


@router.get("/{tconst}")
def get_title(tconst: str, db: Session = Depends(get_db)):
	return db.query(TitleBasic).filter(TitleBasic.tconst == tconst).first()
