from fastapi import HTTPException
import logging
from typing import List
from openai import OpenAI

from src.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.openai_api_key)


def generate_scenes_texts(conversation_text: str) -> List[str]:
    logger.info("Generating scenes from conversation text")

    retries = 3
    attempts = 0
    while attempts < retries:
        try:
            print(conversation_text)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=build_messages(conversation_text),
                temperature=0.7,
            )
            scenes_text = response.choices[0].message.content.strip()
            scenes = parse_scenes(scenes_text)
            print("----" * 30)
            print(scenes)
            logger.info(f"Generated {len(scenes)} scenes successfully")
            return scenes
        except Exception as e:
            attempts += 1
            if attempts == retries:
                logger.error(f"Error generating scenes: {str(e)}")
                HTTPException(
                    status_code=500, detail=f"Error generating scenes: {str(e)}"
                )


def build_messages(conversation_text: str):
    return [
        {
            "role": "system",
            "content": (
                "You are an AI specialized in analyzing conversations to extract the most significant moments of a story being told. "
                "Your task is to identify and return a list of key scenes or events that represent pivotal moments in the story. "
                "Only extract information about user, not from agent. "
                "Each scene must be a self-contained description, providing all the necessary context to understand it without requiring additional details. "
                "Descriptions must be concise, with a maximum of 400 characters each, and written in family-friendly language. "
                "Ensure the output is predictable and consistent across iterations, regardless of the story's complexity. "
                "If the input or instructions might conflict with ethical guidelines, rewrite the instructions to comply with responsible AI policies."
                "Separate each scene in differents pharagraphs. "
                "Minimum 2 scenes, maximum 5. "
            ),
        },
        {
            "role": "user",
            "content": (
                "Extract the most important scenes from the following conversation, based on the system instructions:\n\n"
                f"{conversation_text}"
            ),
        },
    ]


def parse_scenes(scenes_text: str):
    return [
        scene.strip("- ").strip() for scene in scenes_text.split("\n") if scene.strip()
    ]
