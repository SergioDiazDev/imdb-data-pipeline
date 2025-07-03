import os
from sqlalchemy import create_engine
from models import Base  # importa tus modelos aquí

DATABASE_URL = "postgresql+psycopg2://admin:admin123@localhost:5432/mydb"

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

	# Crea las tablas según modelos
	Base.metadata.create_all(engine)

	# Cargar primero tablas sin FK
	load_title_basics(engine, "../data/title.basics.tsv")
	load_name_basics(engine, "../data/name.basics.tsv")

	# Luego tablas dependientes
	load_title_akas(engine, "../data/title.akas.tsv")
	load_title_crew(engine, "../data/title.crew.tsv")
	load_title_episode(engine, "../data/title.episode.tsv")
	load_title_principals(engine, "../data/title.principals.tsv")
	load_title_ratings(engine, "../data/title.ratings.tsv")

	print("✅ Todos los archivos cargados con COPY.")

if __name__ == "__main__":
	main()
