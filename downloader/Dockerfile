FROM python:3.14.0b3-slim-bullseye

WORKDIR /imdb-data-pipeline

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "download.py", "-o", "/imdb-data-pipeline/data"]