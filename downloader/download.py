import sys
from pathlib import Path

from utils import load_config, download_and_decompress


def main():

	# Cargamos la configuración
	config = load_config()
	
	base_url = config["base_url"]
	datasets = config["datasets"]
	dest_dir = Path(config["dest_dir"])

	# Aseguramos que el directorio destino existe
	dest_dir.mkdir(parents=True, exist_ok=True)

	# Descargamos y descomprimimos cada dataset
	for dataset in datasets:
		try:
			download_and_decompress(dataset, dest_dir, base_url)
		except Exception as e:
			print(f"\n‼ Error descargando {dataset}: {e}", file=sys.stderr)

	# Creo un archivo download.done para indicar que la descarga ha finalizado
	done_file = dest_dir / "downloader.done"
	done_file.touch()

if __name__ == "__main__":
	main()
