import os
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
	f"postgresql+psycopg2://"
	f"{os.getenv('POSTGRES_USER')}:"
	f"{os.getenv('POSTGRES_PASSWORD')}@"
	f"{os.getenv('POSTGRES_HOST')}:"
	f"{os.getenv('POSTGRES_PORT')}/"
	f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)
# Create the database tables if they do not exist
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	db: Session = SessionLocal()
	try:
		yield db
	finally:
		db.close()