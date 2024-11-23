import logging
import boto3
from sqlmodel import Session

from src.schemas.ai_scene import AIScene
from src.services.aws import save_image_to_s3, bedrock_generate_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = boto3.client("bedrock-runtime", region_name="us-east-1")


def generate_scene_image(scene: str, idx: int, transcription_id: int, session: Session):
    prompt = generate_prompt(scene)

    image_buffer = bedrock_generate_image(prompt)
    image_key = save_image_to_s3(image_buffer, f"scene_{transcription_id}_{idx+1}.png")
    new_scene = AIScene(
        index=idx,
        image_key=image_key,
        transcription_id=transcription_id,
    )
    session.add(new_scene)
    return


def generate_prompt(scene: str) -> str:
    return f"Minimalistic, cartoon, draw, description: {scene}"
