from fastapi import FastAPI

from src.routers import onboarding, users, observations

app = FastAPI()


app.include_router(onboarding.router)
app.include_router(users.router)
app.include_router(observations.router)


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
