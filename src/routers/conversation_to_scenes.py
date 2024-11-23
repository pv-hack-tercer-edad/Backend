import logging
from fastapi import APIRouter
from src.comands.scenes.index import generate_scenes
from src.schemas.convesation import ConversationRequest, ConversationResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.post("/process-conversation", response_model=ConversationResponse)
async def process_conversation(
    conversation: ConversationRequest,
) -> ConversationResponse:
    logger.info("Starting conversation processing")
    processed_scenes = generate_scenes(conversation)

    return ConversationResponse(images=processed_scenes)
