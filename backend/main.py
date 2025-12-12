from fastapi import FastAPI
from database import engine, Base
from routers import auth, users, products, articles
from fastapi.staticfiles import StaticFiles
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../frontend")),
    name="static"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(articles.router)

# python -m uvicorn main:app --reload