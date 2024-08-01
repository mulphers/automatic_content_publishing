from typing import Optional

from pydantic import BaseModel


class ContentDTO(BaseModel):
    content_id: int
    url: str
    description: Optional[str] = None


class ContentCreate(ContentDTO):
    pass


class ContentUpdate(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None
