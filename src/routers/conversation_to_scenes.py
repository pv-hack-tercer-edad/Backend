import logging
from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from src.routers.video import generate_video
from src.schemas.chapter import Chapter
from src.comands.scenes.index import generate_scenes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversation", tags=["conversation"])


async def process_conversation(
    chapter_id: int,
    session: Session,
) -> None:

    chapter = session.get(Chapter, chapter_id)
    logger.info(f"Starting conversation processing chapter:{chapter_id}")
    chapter.status = "PROCESSING"
    session.commit()
    session.refresh(chapter)

    retry = 5
    attempt = 0
    while attempt < retry:
        try:
            generate_scenes(
                chapter.transcription.content, chapter.transcription.id, session
            )
            break
        except Exception as e:
            attempt += 1
            if attempt >= retry:
                logger.error(f"Error processing conversation: {str(e)}")
                session.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Error processing conversation: {str(e)}"
                )
    await generate_video(chapter_id, session)
