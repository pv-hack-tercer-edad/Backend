from io import BytesIO
from uuid import uuid4

import requests
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
import logging
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/videos")


def download_image(url: str) -> str:
    """Download an image from a URL and return the local file path."""
    response = requests.get(url)
    response.raise_for_status()
    temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
    with open(temp_file.name, "wb") as f:
        f.write(response.content)
    return temp_file.name


def create_video_with_audio(images: list[str], audio_path: str, output_path: str):
    """Create an MP4 video with transitions between images and background audio."""
    # Load audio to calculate the duration for each image
    audio = AudioFileClip(audio_path)
    total_audio_duration = audio.duration
    logger.info(f"Audio duration: {total_audio_duration}")

    # Calculate duration per image
    if len(images) == 0:
        raise HTTPException("No images provided")

    duration_per_image = total_audio_duration / len(images)
    logger.info(f"Duration per image: {duration_per_image} seconds")

    # Load images and set duration
    clips = [ImageClip(img).set_duration(duration_per_image) for img in images]

    # Add crossfade transition between clips
    video = concatenate_videoclips(clips, method="compose")

    # Set audio and synchronize duration
    video = video.set_audio(audio).set_duration(audio.duration)
    logger.info(f"Video duration: {video.duration}")

    # Write video to file
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")


@router.post("/generate")
async def generate_video(
    images: list[str] = Form(...),
    audio: UploadFile = File(...),
):
    try:
        # Save audio file temporarily
        audio_temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        logger.info(f"Writing audio to {audio_temp_file.name}")
        with open(audio_temp_file.name, "wb") as f:
            f.write(await audio.read())
        logger.info(f"Wrote audio to {audio_temp_file.name}")

        # Download images
        image_paths = [download_image(uri) for uri in images]
        logger.info(f"Downloaded {len(image_paths)} images")

        # Check if images were provided
        if not image_paths:
            raise HTTPException(status_code=400, detail="No images provided")

        # Create the video
        output_path = f"{uuid4()}.mp4"
        logger.info(f"Creating video at {output_path}")
        create_video_with_audio(image_paths, audio_temp_file.name, output_path)
        logger.info(f"Created video at {output_path}")

        # Return the video as a streaming response
        return StreamingResponse(
            open(output_path, "rb"),
            media_type="video/mp4",
            headers={"Content-Disposition": f"attachment; filename={output_path}"},
        )
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
