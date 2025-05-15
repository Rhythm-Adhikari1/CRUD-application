from fastapi import FastAPI
from .routers import posts

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


app.include_router(posts.router)
