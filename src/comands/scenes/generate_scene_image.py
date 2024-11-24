import logging
import boto3
from fastapi import HTTPException
from sqlmodel import Session

from src.schemas.ai_scene import AIScene
from src.services.aws import save_image_to_s3, bedrock_generate_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = boto3.client("bedrock-runtime", region_name="us-east-1")

MAX_RETRIES = 3


def generate_scene_image(scene: str, idx: int, transcription_id: int, session: Session):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            taskType = get_taskType(idx)
            prompt = generate_prompt(scene)
            if len(prompt) > 511:
                prompt = prompt[:511]
            image_buffer = bedrock_generate_image(prompt, taskType)
            image_key = save_image_to_s3(
                image_buffer, f"scene_{transcription_id}_{idx+1}.png"
            )
            new_scene = AIScene(
                index=idx,
                image_link=image_key,
                transcription_id=transcription_id,
            )
            session.add(new_scene)
            return
        except Exception as e:
            logger.error(f"Error generating scene image: {str(e)}")
            logger.error(f"Retrying scene image generation: {retries}/{MAX_RETRIES}")
            retries += 1
    if retries == MAX_RETRIES:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error generating scene image")


def generate_prompt(scene: str) -> str:
    return f"Minimalistic, cartoon, draw, description: {scene}"


def get_taskType(idx: int):
    return "TEXT_IMAGE"
    if idx == 0:
        return "TEXT_IMAGE"
    return "IMAGE_VARIATION"
