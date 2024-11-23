from fastapi import FastAPI

from src.routers import (
    onboarding,
    users,
    observations,
    ficha,
    vital_signs,
    vital_signs_history,
)

app = FastAPI()


app.include_router(onboarding.router)
app.include_router(users.router)
app.include_router(observations.router)
app.include_router(ficha.router)
app.include_router(vital_signs.router)
app.include_router(vital_signs_history.router)


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
