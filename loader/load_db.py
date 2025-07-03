import os
from sqlalchemy import create_engine, text
from models import Base  # importa tus modelos aquí

DATABASE_URL = (
	f"postgresql+psycopg2://"
	f"{os.getenv('POSTGRES_USER')}:"
	f"{os.getenv('POSTGRES_PASSWORD')}@"
	f"{os.getenv('POSTGRES_HOST')}:"
	f"{os.getenv('POSTGRES_PORT')}/"
	f"{os.getenv('POSTGRES_DB')}"
)
DATA_DIR = os.getenv('DATA_DIR')

def disable_fks_and_triggers(engine, table_names):
	with engine.connect() as conn:
		for table in table_names:
			conn.execute(text(f'ALTER TABLE "{table}" DISABLE TRIGGER ALL;'))
		conn.commit()

def enable_fks_and_triggers(engine, table_names):
	with engine.connect() as conn:
		for table in table_names:
			conn.execute(text(f'ALTER TABLE "{table}" ENABLE TRIGGER ALL;'))
		conn.commit()


def quote_col(col: str) -> str:
	# Si la columna tiene mayúsculas, ponla entre comillas dobles
	# PostgreSQL diferencia mayúsculas y minúsculas si están entre comillas
	if any(c.isupper() for c in col):
		return f'"{col}"'
	return col

def quote_table(table_name: str) -> str:
	# Siempre poner entre comillas para evitar problemas
	return f'"{table_name}"'

def copy_from_tsv(engine, path, table_name, columns, delimiter='\t', null_str='\\N'):
	conn = engine.raw_connection()
	cursor = conn.cursor()
	try:
		with open(path, 'r', encoding='utf-8') as f:
			cols = ', '.join(quote_col(c) for c in columns)
			tbl = quote_table(table_name)
			sql = f"""COPY {tbl}({cols})
			FROM STDIN WITH (
				FORMAT text,
				DELIMITER E'\\t',
				NULL '{null_str}',
				HEADER true
			)
			"""
			cursor.copy_expert(sql, f)
		conn.commit()
		print(f"✅ Carga con COPY para {table_name} finalizada correctamente.")
	except Exception as e:
		conn.rollback()
		print(f"❌ Error en COPY para {table_name}: {e}")
	finally:
		cursor.close()
		conn.close()

def load_name_basics(engine, path):
	columns = [
		'nconst',
		'primaryName',
		'birthYear',
		'deathYear',
		'primaryProfession',
		'knownForTitles'
	]
	copy_from_tsv(engine, path, 'name_basics', columns)

def load_title_basics(engine, path):
	columns = [
		'tconst',
		'titleType',
		'primaryTitle',
		'originalTitle',
		'isAdult',
		'startYear',
		'endYear',
		'runtimeMinutes',
		'genres'
	]
	copy_from_tsv(engine, path, 'title_basics', columns)

def load_title_akas(engine, path):
	columns = [
		'titleId',
		'ordering',
		'title',
		'region',
		'language',
		'types',
		'attributes',
		'isOriginalTitle'
	]
	copy_from_tsv(engine, path, 'title_akas', columns)

def load_title_crew(engine, path):
	columns = [
		'tconst',
		'directors',
		'writers'
	]
	copy_from_tsv(engine, path, 'title_crew', columns)

def load_title_episode(engine, path):
	columns = [
		'tconst',
		'parentTconst',
		'seasonNumber',
		'episodeNumber'
	]
	copy_from_tsv(engine, path, 'title_episode', columns)

def load_title_principals(engine, path):
	columns = [
		'tconst',
		'ordering',
		'nconst',
		'category',
		'job',
		'characters'
	]
	copy_from_tsv(engine, path, 'title_principals', columns)

def load_title_ratings(engine, path):
	columns = [
		'tconst',
		'averageRating',
		'numVotes'
	]
	copy_from_tsv(engine, path, 'title_ratings', columns)

def main():
	engine = create_engine(DATABASE_URL, echo=True)

	# Crea las tablas según modelos y las trunca si existen
	Base.metadata.drop_all(engine)  # Elimina tablas existentes
	Base.metadata.create_all(engine)

	# Cargar primero tablas sin FK
	load_title_basics(engine, f"{DATA_DIR}/title.basics.tsv")
	load_name_basics(engine, f"{DATA_DIR}/name.basics.tsv")

	dependent_tables = [
		"title_akas",
		"title_crew",
		"title_episode",
		"title_principals",
		"title_ratings"
	]
	disable_fks_and_triggers(engine, dependent_tables)

	# Luego tablas dependientes
	load_title_akas(engine, f"{DATA_DIR}/title.akas.tsv")
	load_title_crew(engine, f"{DATA_DIR}/title.crew.tsv")
	load_title_episode(engine, f"{DATA_DIR}/title.episode.tsv")
	load_title_principals(engine, f"{DATA_DIR}/title.principals.tsv")
	load_title_ratings(engine, f"{DATA_DIR}/title.ratings.tsv")

	print("✅ Todos los archivos cargados con COPY.")

	enable_fks_and_triggers(engine, dependent_tables)

	with engine.connect() as conn:
		conn.execute(text("CHECKPOINT;"))
		conn.commit()

if __name__ == "__main__":
	main()
