from dataclasses import dataclass


@dataclass
class ExternalReferenceMessage:
    name: str
    description: str | None = None
    url: str | None = None
    extrernal_id: str | None = None
    reference_id: str | None = None
