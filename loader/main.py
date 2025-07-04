import os
from sqlalchemy import create_engine, text
from models import Base
from utils import disable_fks_and_triggers, enable_fks_and_triggers
from load_db import (
	load_title_basics, load_name_basics, load_title_akas,
	load_title_crew, load_title_episode, load_title_principals,
	load_title_ratings
)

def main():

	DATABASE_URL = (
		f"postgresql+psycopg2://"
		f"{os.getenv('POSTGRES_USER')}:" 
		f"{os.getenv('POSTGRES_PASSWORD')}@"
		f"{os.getenv('POSTGRES_HOST')}:" 
		f"{os.getenv('POSTGRES_PORT')}/" 
		f"{os.getenv('POSTGRES_DB')}"
	)

	engine = create_engine(DATABASE_URL, echo=True)

	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	load_title_basics(engine, f"{os.getenv('DATA_DIR')}/title.basics.tsv")
	load_name_basics(engine, f"{os.getenv('DATA_DIR')}/name.basics.tsv")

	dependent_tables = [
		"title_akas", "title_crew", "title_episode", "title_principals", "title_ratings"
	]
	disable_fks_and_triggers(engine, dependent_tables)

	load_title_akas(engine, f"{os.getenv('DATA_DIR')}/title.akas.tsv")
	load_title_crew(engine, f"{os.getenv('DATA_DIR')}/title.crew.tsv")
	load_title_episode(engine, f"{os.getenv('DATA_DIR')}/title.episode.tsv")
	load_title_principals(engine, f"{os.getenv('DATA_DIR')}/title.principals.tsv")
	load_title_ratings(engine, f"{os.getenv('DATA_DIR')}/title.ratings.tsv")

	print("✅ Todos los archivos cargados con COPY.")

	enable_fks_and_triggers(engine, dependent_tables)

	with engine.connect() as conn:
		conn.execute(text("CHECKPOINT;"))
		conn.commit()

if __name__ == "__main__":
	main()
