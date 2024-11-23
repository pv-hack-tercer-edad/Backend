from typing import List
from pydantic import BaseModel


class ConversationRequest(BaseModel):
    text: str


class SceneImage(BaseModel):
    scene: str
    image_key: str


class ConversationResponse(BaseModel):
    images: List[SceneImage]
