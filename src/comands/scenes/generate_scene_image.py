import logging
import os
import boto3
from src.schemas.convesation import SceneImage
from src.services.aws import save_image_to_s3, bedrock_generate_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = boto3.client("bedrock-runtime", region_name="us-east-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def generate_scene_image(scene: str, idx: int):
    prompt = generate_prompt(scene)

    image_buffer = bedrock_generate_image(prompt)
    image_key = save_image_to_s3(image_buffer, f"scene_{idx+1}.png")
    return SceneImage(scene=scene, image_key=image_key)


def generate_prompt(scene: str) -> str:
    return f"Minimalistic, cartoon, draw, description: {scene}"
