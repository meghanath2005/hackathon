from pydantic import BaseModel


class CycloneSummary(BaseModel):
    cyclone_id: str
    name: str
    season: int
    basin: str


class CyclonesResponse(BaseModel):
    cyclones: list[CycloneSummary]
