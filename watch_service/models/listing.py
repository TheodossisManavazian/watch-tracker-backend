from datetime import datetime
from pydantic import BaseModel


class Listing(BaseModel):
    hash_id: str
    listing_url: str
    reference_number: str
    price_usd: float
    original_price: float
    original_currency: str
    exchange_rate: float
    listing_code: str | None = None
    brand: str | None = None
    model: str | None = None
    dial: str | None = None
    year: str | None = None
    condition: str | None = None
    accessories: str | None = None
    location: str | None = None
    updated_at: datetime | None = None

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())
