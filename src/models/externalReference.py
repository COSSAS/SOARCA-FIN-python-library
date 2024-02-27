from typing import Optional
from pydantic import BaseModel


class ExternalReference(BaseModel):
    name: str
    description: Optional[str]
    source: Optional[str]
    url: Optional[str]
    external_id: Optional[str]
    reference_id: Optional[str]
