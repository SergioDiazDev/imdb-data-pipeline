from sqlalchemy import text

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
	if any(c.isupper() for c in col):
		return f'"{col}"'
	return col

def quote_table(table_name: str) -> str:
	return f'"{table_name}"'
