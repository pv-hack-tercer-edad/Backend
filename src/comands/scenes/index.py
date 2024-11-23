from fastapi import HTTPException
import logging
from sqlmodel import Session
from typing import List

from src.comands.scenes.generate_scenes_text import generate_scenes_texts
from src.comands.scenes.generate_scene_image import generate_scene_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_scenes(text: str, transcription_id: int, session: Session):
    scenes_texts = generate_scenes_texts(text)
    scenes_images = generate_scenes_images(scenes_texts, transcription_id, session)
    logger.info(f"Successfully generated {len(scenes_texts)} scenes")
    return scenes_images


def generate_scenes_images(scenes: List[str], transcription_id: int, session: Session):
    processed_scenes = []
    for idx, scene in enumerate(scenes):
        logger.info(f"Processing scene {idx + 1}/{len(scenes)}")
        try:
            image = generate_scene_image(scene, idx, transcription_id, session)
            processed_scenes.append(image)
            logger.info(f"Successfully processed scene {idx + 1}")
        except Exception as e:
            logger.error(f"Error processing scene {idx + 1}: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error processing scene {idx+1}: {str(e)}"
            )
    return processed_scenes
