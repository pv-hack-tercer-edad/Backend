import aiohttp
import aiofiles
from io import BytesIO
from uuid import uuid4
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from pydantic import BaseModel, HttpUrl
from typing import List
import logging
import os
from tempfile import NamedTemporaryFile

from sqlmodel import Session

from src.services.aws import save_video_to_s3
from src.config.settings import settings
from src.schemas.chapter import Chapter
from src.config.db import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/videos", tags=["videos"])


class VideoPayloadItem(BaseModel):
    url_image: str
    url_sound: str


class VideoPayload(BaseModel):
    items: List[VideoPayloadItem]


async def download_file_async(url: str, suffix: str) -> str:
    """Asynchronously download a file from a URL and save it locally."""
    logger.info(f"Downloading {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Failed to download {url}")
            temp_file = NamedTemporaryFile(delete=False, suffix=suffix)
            async with aiofiles.open(temp_file.name, "wb") as f:
                await f.write(await response.read())
            return temp_file.name


async def process_video_pair(image_path: str, sound_path: str, index: int, total: int) -> ImageClip:
    """Process a single image-audio pair to generate a video clip."""
    # Offload CPU-bound processing to a thread
    return await asyncio.to_thread(create_video_from_image_and_audio, image_path, sound_path, index, total)


def create_video_from_image_and_audio(image_path: str, audio_path: str, index: int, total: int) -> ImageClip:
    """Synchronously create a video clip from an image and audio."""
    # Load audio to calculate duration
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    print(f"audio duration: {audio_duration}")
    print(f"start: {index / total * audio_duration}")
    print(f"duration: {audio_duration / total}")
    audio_clip = audio_clip.set_start(index / total * audio_duration).set_duration(audio_duration / total)

    # Create an image clip and set duration
    # image_clip = ImageClip(image_path).set_duration(audio_duration)
    image_clip = ImageClip(image_path).set_start(index / total * audio_duration).set_duration(audio_duration / total)

    # Set the audio to the image clip
    return image_clip.set_audio(audio_clip)


async def concatenate_videos_async(video_clips: List[ImageClip]) -> str:
    """Concatenate video clips asynchronously and save to a file."""
    output_path = f"{uuid4()}.mp4"
    print(f"The output path is {output_path}")
    # Offload concatenation to a thread
    if len(video_clips) > 1:
        await asyncio.to_thread(
            lambda: concatenate_videoclips(video_clips, method="compose").write_videofile(
                output_path, fps=24, codec="libx264", audio_codec="aac"
            )
        )
    else:
        video_clips[0].write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    return output_path


# @router.post("/generate/{chapter_id}")
async def generate_video(chapter_id: int, session: Session):
    """
    Generate a video by merging multiple image and audio pairs, and concatenating the resulting videos.

    Payload: list of {"url_image": str, "url_sound": str}
    """
    try:
        chapter = session.get(Chapter, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        # List to store video clips
        video_clips = []

        # Download all files and process each image-audio pair
        print(f"chapter.transcription.ai_scenes: {chapter.transcription.ai_scenes}")
        tasks = [
            download_file_async(f"{settings.aws_s3_bucket_url}/{scene.image_link}", ".png")
            for scene in chapter.transcription.ai_scenes
        ]
        tasks.append(download_file_async(chapter.transcription.recording_link, ".wav"))

        # Await downloads
        downloaded_files = await asyncio.gather(*tasks)
        image_paths = [path for path in downloaded_files if path.endswith(".png")]
        sound_path = [path for path in downloaded_files if path.endswith(".wav")][0]
        print(f"image_paths: {image_paths}")
        print(f"sound_path: {sound_path}")

        # Process video pairs
        for index, image_path in enumerate(image_paths):
            print(f"image_path: {image_path}")
            print(f"sound_path: {sound_path}")
            video_clip = await process_video_pair(image_path, sound_path, index, len(image_paths))
            print(f"the video clip is {video_clip}")
            video_clips.append(video_clip)

        # Concatenate all video clips
        print(f"video_clips: {video_clips}")
        for video_clip in video_clips:
            print(f"duration: {video_clip.duration}")
            print(f"start: {video_clip.start}")
            print(f"end: {video_clip.end}")
        output_path = await concatenate_videos_async(video_clips)

        with open(output_path, "rb") as f:
            video_link = save_video_to_s3(f.read(), f"video_{chapter_id}.mp4")
        chapter.video_link = f"{settings.aws_s3_bucket_url}/{video_link}"
        chapter.status = "DONE"
        session.commit()
        # Clean up temporary files
        for path in downloaded_files:
            os.remove(path)
        return video_link
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}", exc_info=True)
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
