from fastapi import FastAPI
from app.routers import titles, people, control, akas

app = FastAPI()

app.include_router(control.router)
app.include_router(titles.router)
app.include_router(akas.router)
app.include_router(people.router)
