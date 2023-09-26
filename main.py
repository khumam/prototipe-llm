from fastapi import FastAPI
from app.routers import routers

app = FastAPI(
  title="LLM Prototipe",
  description="LLM Propotipe to query from datasource"
)

app.include_router(routers)

@app.on_event("startup")
def on_startup():
  return