import logging
from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from src.routers.video import generate_video
from src.schemas.chapter import Chapter
from src.schemas.transcription import Transcription
from src.comands.scenes.index import generate_scenes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversation", tags=["conversation"])


# @router.post("/process-conversation/{chapter_id}")
async def process_conversation(
    chapter_id: int,
    session: Session,
) -> None:
    try:
        chapter = session.get(Chapter, chapter_id)
        logger.info(f"Starting conversation processing chapter:{chapter_id}")
        new_transcription = Transcription(
            text=chapter.transcription.content,
            chapter_id=chapter_id,
        )
        chapter.status = "PROCESSING"
        session.add(new_transcription)
        session.commit()
        session.refresh(chapter)
        print(new_transcription)
        generate_scenes(new_transcription.content, new_transcription.id, session)
        await generate_video(chapter_id, session)
    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error processing conversation: {str(e)}"
        )
