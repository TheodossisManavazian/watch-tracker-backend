from pydantic import BaseModel


class Caliber(BaseModel):
    caliber: str
    brand: str
    movement: str
    power_reserve: str | None
    qty_jewels: str | None
    frequency: str | None

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())