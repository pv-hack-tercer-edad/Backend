from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from retell import Retell
from sqlmodel import Session

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


@router.get("/get-call")
def get_call(
    call_id: str,
    chapter_id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    client = Retell(
        api_key=settings.retell_ai_api_key,
    )
    web_call_response = client.call.retrieve(call_id)
    chapter = session.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    new_transcription = Transcription(
        text=web_call_response.transcript,
        chapter_id=chapter_id,
    )
    chapter.transcription = new_transcription
    session.add(chapter)
    session.add(new_transcription)
    session.commit()
    session.refresh(chapter)
    background_tasks.add_task(process_conversation, chapter_id, session)
    return chapter