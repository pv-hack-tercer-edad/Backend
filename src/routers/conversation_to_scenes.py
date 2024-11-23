import logging
import os
from typing import List

import boto3
import requests
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversation", tags=["conversation"])

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

logger.info(f"Initialized router with bucket: {BUCKET_NAME}")


class ConversationRequest(BaseModel):
    text: str


class SceneImage(BaseModel):
    scene: str
    image_key: str


class ConversationResponse(BaseModel):
    images: List[SceneImage]


def generate_scenes(conversation_text: str) -> List[str]:
    logger.info("Generating scenes from conversation text")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that extracts key scenes from conversations. Return only the scenes with detailed descriptions, one per line.",
                },
                {
                    "role": "user",
                    "content": f"From the following conversation between an elderly man and an AI assistant, extract key scenes that depict significant moments in the man's life. Provide each scene as a detailed description:\n\n{conversation_text}",
                },
            ],
            temperature=0.7,
        )
        scenes_text = response.choices[0].message.content.strip()
        scenes = [
            scene.strip("- ").strip()
            for scene in scenes_text.split("\n")
            if scene.strip()
        ]

        logger.info(f"Generated {len(scenes)} scenes successfully")
        return scenes
    except Exception as e:
        logger.error(f"Error generating scenes: {str(e)}")
        raise


def generate_dalle_prompt(scene_description: str) -> str:
    prompt = f"An artistic depiction of the following scene: {scene_description}"
    logger.debug(f"Generated DALL-E prompt: {prompt}")
    return prompt


def generate_image(prompt: str) -> str:
    logger.info("Generating image with DALL-E")
    try:
        response = client.images.generate(prompt=prompt, n=1, size="1024x1024")
        image_url = response.data[0].url
        logger.info(f"Successfully generated image: {image_url[:50]}...")
        return image_url
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise


def save_image_to_s3(image_url: str, image_name: str) -> str:
    logger.info(f"Saving image to S3: {image_name}")
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            error_msg = f"Failed to download image from {image_url}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=image_name,
            Body=response.content,
            ContentType="image/png",
        )
        logger.info(f"Successfully saved image to S3: {image_name}")
        return image_name
    except Exception as e:
        logger.error(f"Error saving image to S3: {str(e)}")
        raise


@router.post("/process-conversation", response_model=ConversationResponse)
async def process_conversation(
    conversation: ConversationRequest,
) -> ConversationResponse:
    logger.info("Starting conversation processing")
    try:
        scenes = generate_scenes(conversation.text)
        logger.info(f"Successfully generated {len(scenes)} scenes")
    except Exception as e:
        logger.error(f"Failed to generate scenes: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error generating scenes: {str(e)}"
        )

    processed_scenes = []
    for idx, scene in enumerate(scenes):
        logger.info(f"Processing scene {idx + 1}/{len(scenes)}")
        try:
            prompt = generate_dalle_prompt(scene)
            image_url = generate_image(prompt)
            image_key = save_image_to_s3(image_url, f"scene_{idx+1}.png")
            processed_scenes.append(SceneImage(scene=scene, image_key=image_key))
            logger.info(f"Successfully processed scene {idx + 1}")
        except Exception as e:
            logger.error(f"Error processing scene {idx + 1}: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Error processing scene {idx+1}: {str(e)}"
            )

    logger.info("Completed processing all scenes successfully")
    return ConversationResponse(images=processed_scenes)
