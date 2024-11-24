from fastapi import FastAPI

from src.routers import (
    users,
    transcription,
    story,
    chapter,
    conversation_to_scenes,
    ai_scene,
    video,
    retell,
)
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(story.router)
app.include_router(transcription.router)
app.include_router(chapter.router)
app.include_router(video.router)
app.include_router(conversation_to_scenes.router)
app.include_router(ai_scene.router)
app.include_router(retell.router)


@app.get("/")
async def root():
    return {"message": "Hello World from Platanus Hack 🍌!"}
