# imdb_ingest/utils.py

import requests
import gzip
import shutil
from pathlib import Path
import yaml
import hashlib

def load_config(config_path: Path = Path("config.yml")) -> dict:
	"""
	Carga la configuración desde un archivo YAML.
	Por defecto, busca 'config.yml' en el directorio actual.
	"""
	with open(config_path, "r") as f:
		return yaml.safe_load(f)


def download(name: str, dest_dir: Path, base_url: str) -> Path:
	"""
	Descarga un archivo IMDb .tsv.gz y lo guarda en el directorio destino solo si cambia.
	"""
	url = f"{base_url}/{name}.tsv.gz"
	compressed_path = dest_dir / f"{name}.tsv.gz"
	decompressed_path = dest_dir / f"{name}.tsv"
	hash_path = dest_dir / f"{name}.tsv.gz.sha256"

	# Comprobar si el hash remoto y local coinciden
	if compressed_path.exists() and hash_path.exists():
		if comparar_hash_remoto_vs_local(url, hash_path):
			print(f"→ {name}.tsv.gz ya está actualizado, no se descarga.")
			return decompressed_path if decompressed_path.exists() else decompressed_path

	# Descargar el archivo
	print(f"→ Descargando {url} …")
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(compressed_path, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)
	print(" OK")

	# Guardar hash
	save_file_hash(compressed_path, hash_path)

	return decompressed_path

def download_and_decompress(name: str, dest_dir: Path, base_url: str) -> Path:
	"""
	Descarga un archivo IMDb .tsv.gz, lo descomprime y guarda el archivo descomprimido en el directorio destino.
	Si el archivo ya existe y no ha cambiado, no se vuelve a descargar.
	Devuelve la ruta al archivo descomprimido (.tsv).
	"""
	url = f"{base_url}/{name}.tsv.gz"
	compressed_path = dest_dir / f"{name}.tsv.gz"
	decompressed_path = dest_dir / f"{name}.tsv"
	etag_path = compressed_path.with_suffix(compressed_path.suffix + ".etag")

	print(f"compressed_path: {compressed_path}, decompressed_path: {decompressed_path}, etag_path: {etag_path}")
	if compressed_path.exists() and etag_path.exists():
		print(f"→ Comprobando si {name}.tsv.gz ha cambiado …")
		if comparar_etag_local_vs_remoto(url, etag_path):
			print(f"→ {name}.tsv.gz ya está actualizado, no se descarga.")
			return decompressed_path if decompressed_path.exists() else decompressed_path
		else:
			print(f"→ {name}.tsv.gz ha cambiado, se descarga de nuevo.")

	print(f"→ Descargando {url} …")
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(compressed_path, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)
	print("OK")

	etag_remoto = obtener_etag_remoto(url)
	if etag_remoto:
		etag_path.write_text(etag_remoto)

	print(f"→ Descomprimiendo {compressed_path} …")
	with gzip.open(compressed_path, "rb") as f_in:
		with open(decompressed_path, "wb") as f_out:
			shutil.copyfileobj(f_in, f_out)
	print("OK")

	compressed_path.unlink()
	return decompressed_path

def obtener_etag_remoto(url: str) -> str | None:
	"""
	Obtiene el ETag del recurso remoto especificado por la URL.
	Devuelve el ETag como cadena o None si no se pudo obtener.
	"""
	try:
		r = requests.head(url)
		r.raise_for_status()
		return r.headers.get("ETag")
	except Exception:
		return None


def comparar_etag_local_vs_remoto(url: str, etag_local_path: Path) -> bool:
	"""
	Compara el ETag del archivo remoto con el guardado localmente.
	Devuelve True si coinciden, False si no o no existe local.
	"""
	if not etag_local_path.exists():
		return False

	etag_local = etag_local_path.read_text().strip()
	etag_remoto = obtener_etag_remoto(url)

	if etag_remoto is None:
		# No se pudo obtener ETag, forzar descarga
		return False

	return etag_local == etag_remoto