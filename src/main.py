from fastapi import FastAPI

from routers import onboarding

app = FastAPI()


app.include_router(onboarding.router)

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}