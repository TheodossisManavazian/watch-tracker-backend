from datetime import datetime
from pydantic import BaseModel


class Watch(BaseModel):
    reference_number: str
    brand: str
    years_produced: str | None = None
    description: str | None = None
    model: str | None = None
    pricing: dict | None = None
    case_info: dict | str | None = None
    dial: str | None = None
    bracelet_info: dict | None = None
    caliber: str | None = None
    nickname: str | None = None
    updated_at: datetime | None = None

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())