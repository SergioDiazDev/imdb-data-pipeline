from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import NameBasic
from app.db import get_db

router = APIRouter(prefix="/people", tags=["People"])

@router.get("/{nconst}")
def get_person(nconst: str, db: Session = Depends(get_db)):
	person = db.query(NameBasic).filter(NameBasic.nconst == nconst).first()
	if not person:
		raise HTTPException(status_code=404, detail="Person not found")
	return person
