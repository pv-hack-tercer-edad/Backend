from fastapi import FastAPI

from src.routers import (
    conversation_to_scenes,
    ficha,
    observations,
    onboarding,
    users,
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
app.include_router(conversation_to_scenes.router)


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
