import logging
import boto3
import json
import base64

from src.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
BUCKET_NAME = settings.aws_s3_bucket


def save_video_to_s3(video_buffer: str, video_name: str) -> str:
    logger.info(f"Saving video to S3: {video_name}")
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=video_name,
            Body=video_buffer,
            ContentType="video/mp4",
        )
        logger.info(f"Successfully saved video to S3: {video_name}")
        return video_name
    except Exception as e:
        logger.error(f"Error saving video to S3: {str(e)}")
        raise


def save_image_to_s3(image_buffer: str, image_name: str) -> str:
    logger.info(f"Saving image to S3: {image_name}")
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=image_name,
            Body=image_buffer,
            ContentType="image/png",
        )
        logger.info(f"Successfully saved image to S3: {image_name}")
        return image_name
    except Exception as e:
        logger.error(f"Error saving image to S3: {str(e)}")
        raise


def bedrock_generate_image(prompt: str, taskType: str):
    model_id = "amazon.titan-image-generator-v1"
    native_request = get_bedrock_request(prompt, taskType)
    request = json.dumps(native_request)
    response = bedrock_client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]
    image = base64.b64decode(base64_image_data)
    if taskType == "TEXT_IMAGE":
        write_base_image(image)
    return image


def get_bedrock_request(prompt: str, taskType):
    if taskType == "TEXT_IMAGE":
        return get_text_image_request(prompt)
    return get_image_variation_request(prompt)


def get_text_image_request(prompt: str):
    return {
        "textToImageParams": {"text": prompt},
        "taskType": "TEXT_IMAGE",
        "imageGenerationConfig": {
            "cfgScale": 8,
            "seed": 0,
            "width": 512,
            "height": 512,
            "numberOfImages": 1,
        },
    }


def get_image_variation_request(prompt: str):
    image_base64 = get_base_image()
    return {
        "imageVariationParams": {"images": [image_base64], "text": prompt},
        "taskType": "IMAGE_VARIATION",
        "imageGenerationConfig": {
            "cfgScale": 8,
            "seed": 0,
            "width": 512,
            "height": 512,
            "numberOfImages": 1,
        },
    }


def get_base_image():
    image_base64 = None
    with open("output/base_image.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return image_base64


def write_base_image(image: bytes):
    with open("output/base_image.png", "wb") as image_file:
        image_file.write(image)
