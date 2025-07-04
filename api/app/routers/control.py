from fastapi import APIRouter
import docker

router = APIRouter()
client = docker.from_env()


@router.post("/run-downloader")
def run_downloader():
	try:
		container = client.containers.get("imdb_downloader")
		if container.status != "running":
			container.start()
			return {"status": "downloader started"}
		return {"status": "downloader already running"}
	except docker.errors.NotFound:
		try:
			container = client.containers.run(
				"imdb_downloader",
				name="imdb_downloader",
				detach=True,
				restart_policy={"Name": "no"},
				volumes={
					"/ruta/host/data": {"bind": "/imdb-data-pipeline/data", "mode": "rw"},
				},
			)
			return {"status": "downloader created and started"}
		except docker.errors.APIError as e:
			return {"error": str(e)}


@router.post("/run-loader")
def run_loader():
	try:
		container = client.containers.get("imdb_loader")
		if container.status != "running":
			container.start()
			return {"status": "loader started"}
		return {"status": "loader already running"}
	except docker.errors.NotFound:
		try:
			container = client.containers.run(
				image="imdb_loader",
				name="imdb_loader",
				detach=True,
				restart_policy={"Name": "no"},
				volumes={
					"/ruta/host/data": {"bind": "/imdb-data-pipeline/data", "mode": "rw"},
				},
				environment={
					"DATABASE_URL": "postgresql+psycopg2://admin:admin123@postgres_db:5432/mydb"
				},
			)
			return {"status": "loader created and started"}
		except docker.errors.APIError as e:
			return {"error": str(e)}
