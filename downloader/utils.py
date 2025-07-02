# imdb_ingest/utils.py

import requests
import gzip
import shutil
from pathlib import Path
import yaml


def load_config(config_path: Path = Path("config.yml")) -> dict:
	"""
	Carga la configuración desde un archivo YAML.
	Por defecto, busca 'config.yml' en el directorio actual.
	"""
	with open(config_path, "r") as f:
		return yaml.safe_load(f)


def download(name: str, dest_dir: Path, base_url: str) -> Path:
	"""
	Descarga un archivo IMDb .tsv.gz y lo guarda en el directorio destino.
	"""
	url = f"{base_url}/{name}.tsv.gz"
	compressed_path = dest_dir / f"{name}.tsv.gz"
	decompressed_path = dest_dir / f"{name}.tsv"

	print(f"→ Descargando {url} …")
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(compressed_path, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)
	print(" OK")
	return decompressed_path

def download_and_decompress(name: str, dest_dir: Path, base_url: str) -> Path:
	"""
	Descarga un archivo IMDb .tsv.gz, lo descomprime y guarda el archivo descomprimido en el directorio destino.
	Devuelve la ruta al archivo descomprimido (.tsv).
	"""
	url = f"{base_url}/{name}.tsv.gz"
	compressed_path = dest_dir / f"{name}.tsv.gz"
	decompressed_path = dest_dir / f"{name}.tsv"

	print(f"→ Descargando {url} …")
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(compressed_path, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)
	print("OK")

	print(f"→ Descomprimiendo {compressed_path} …")
	with gzip.open(compressed_path, "rb") as f_in:
		with open(decompressed_path, "wb") as f_out:
			shutil.copyfileobj(f_in, f_out)
	print("OK")

	compressed_path.unlink()
	return decompressed_path
