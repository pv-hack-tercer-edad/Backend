import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from schemas.chapter import Chapter
from src.schemas.transcription import Transcription
from src.config.db import get_session
from src.comands.scenes.index import generate_scenes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.post("/process-conversation/{chapter_id}")
async def process_conversation(
    chapter_id: int,
    session: Session = Depends(get_session),
) -> None:
    try:
        chapter = session.get(Chapter, chapter_id)
        logger.info("Starting conversation processing")
        new_transcription = Transcription(
            text=chapter.transcription.content,
            chapter_id=chapter_id,
        )
        chapter.status = "PROCESSING"
        session.add(new_transcription)
        generate_scenes(chapter.transcription.content, new_transcription.id, session)
        session.commit()
        return
    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error processing conversation: {str(e)}"
        )
