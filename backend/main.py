from fastapi import FastAPI
from database import engine, Base
from routers import auth, users, products, articles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(articles.router)

# python -m uvicorn main:app --reload