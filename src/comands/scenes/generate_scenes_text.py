from fastapi import HTTPException
import logging
from typing import List
from openai import OpenAI
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_scenes_texts(conversation_text: str) -> List[str]:
    logger.info("Generating scenes from conversation text")

    retries = 3
    attempts = 0
    while attempts < retries:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=build_messages(conversation_text),
                temperature=0.7,
            )
            scenes_text = response.choices[0].message.content.strip()
            scenes = parse_scenes(scenes_text)
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
            "content": "You are an assistant that extracts key scenes from conversations. You have to be concise. Return only the scenes with detailed descriptions, one per line with max 400 characters each one",
        },
        {
            "role": "user",
            "content": f"cartoon style, minimalistic, color, simple, based on the following description:\n\n{conversation_text}",
        },
    ]


def parse_scenes(scenes_text: str):
    return [
        scene.strip("- ").strip() for scene in scenes_text.split("\n") if scene.strip()
    ]
