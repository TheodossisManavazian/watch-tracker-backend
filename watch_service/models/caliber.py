from pydantic import BaseModel


class Caliber(BaseModel):
    caliber: str
    brand: str
    movement: str
    power_reserve: str
    qty_jewels: str

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())