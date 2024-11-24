from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from retell import Retell
from sqlmodel import Session
from time import sleep

from src.config.settings import settings
from src.config.db import get_session
from src.routers.conversation_to_scenes import process_conversation
from src.schemas.chapter import Chapter
from src.schemas.transcription import Transcription

router = APIRouter(prefix="/retell", tags=["retell"])


class WebCallRequest(BaseModel):
    category: str


@router.post("/create-web-call")
def create_web_call(
    request: WebCallRequest,
):
    client = Retell(
        api_key=settings.retell_ai_api_key,
    )
    web_call_response = client.call.create_web_call(
        agent_id=settings.retell_ai_agent_id,
        retell_llm_dynamic_variables={"category": request.category},
    )
    return {
        "call_id": web_call_response.call_id,
        "access_token": web_call_response.access_token,
    }


@router.post("/get-call")
def get_call(
    call_id: str,
    chapter_id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    client = Retell(
        api_key=settings.retell_ai_api_key,
    )

    web_call_response_transcript = None
    web_call_response_recording_url = None
    attempt = 1
    while not (web_call_response_transcript and web_call_response_recording_url):
        print(f"attempt to get transcription:{attempt}")
        web_call_response = client.call.retrieve(call_id)
        web_call_response_transcript = web_call_response.transcript
        web_call_response_recording_url = web_call_response.recording_url
        attempt += 1
        sleep(1)
    chapter = session.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    chapter.video_link = None
    if chapter.transcription is None:
        transcription = Transcription(
            chapter_id=chapter_id,
            content=web_call_response.transcript,
            recording_link=web_call_response.recording_url,
        )
        chapter.transcription = transcription
    else:
        transcription = chapter.transcription
        transcription.content = web_call_response.transcript
        transcription.recording_link = web_call_response.recording_url

    session.add(chapter)
    session.add(transcription)
    session.commit()
    session.refresh(chapter)
    background_tasks.add_task(process_conversation, chapter_id, session)
    return chapter
