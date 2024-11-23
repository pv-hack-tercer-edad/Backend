from fastapi import FastAPI

from src.routers import (
    users,
    transcription,
    story,
    chapter,
    conversation_to_scenes,
    ai_scene,
    generative_question,
    video,
)
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


app.include_router(users.router)
app.include_router(story.router)
app.include_router(transcription.router)
app.include_router(chapter.router)
app.include_router(video.router)
app.include_router(conversation_to_scenes.router)
app.include_router(ai_scene.router)
app.include_router(generative_question.router)


@app.get("/")
async def root():
    return {"message": "Hello World from Platanus Hack 🍌!"}
