import logging
import requests
from fastapi import HTTPException
import boto3
import os
import json
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


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


def bedrock_generate_image(prompt: str):
    model_id = "amazon.titan-image-generator-v1"
    native_request = get_bedrock_request(prompt)
    request = json.dumps(native_request)
    response = bedrock_client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    base64_image_data = model_response["images"][0]
    return base64.b64decode(base64_image_data)


def get_bedrock_request(prompt: str):
    image_base64 = get_base_image()
    return {
        "imageVariationParams": {"images": [image_base64], "text": prompt},
        "taskType": "IMAGE_VARIATION",
        "imageGenerationConfig": {
            "cfgScale": 8,
            "seed": 0,
            "width": 1024,
            "height": 1024,
            "numberOfImages": 3,
        },
    }


def get_base_image():
    image_base64 = None
    with open("output/image_2.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return image_base64
