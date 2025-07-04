from utils import quote_col, quote_table

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
	columns = ['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
	copy_from_tsv(engine, path, 'name_basics', columns)

def load_title_basics(engine, path):
	columns = ['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres']
	copy_from_tsv(engine, path, 'title_basics', columns)

# ... más funciones load_title_akas, load_title_crew, etc. igual que antes
def load_title_akas(engine, path):
	columns = ['titleId', 'ordering', 'title', 'region', 'language', 'types', 'attributes', 'isOriginalTitle']
	copy_from_tsv(engine, path, 'title_akas', columns)
	 
def load_title_crew(engine, path):
	columns = ['tconst', 'directors', 'writers']
	copy_from_tsv(engine, path, 'title_crew', columns)
	  
def load_title_episode(engine, path):
	columns = ['tconst', 'parentTconst', 'seasonNumber', 'episodeNumber']
	copy_from_tsv(engine, path, 'title_episode', columns)

def load_title_principals(engine, path):
	columns = ['tconst', 'ordering', 'nconst', 'category', 'job', 'characters']
	copy_from_tsv(engine, path, 'title_principals', columns)

def load_title_ratings(engine, path):
	columns = ['tconst', 'averageRating', 'numVotes']
	copy_from_tsv(engine, path, 'title_ratings', columns)
	