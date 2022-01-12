from fastapi_offline import FastAPIOffline
from . import models
from .database import engine, SessionLocal
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPIOffline()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
