from typing import Optional
from pydantic import BaseModel


class ExternalReference(BaseModel):
    name: str
    description: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    external_id: Optional[str] = None
    reference_id: Optional[str] = None
