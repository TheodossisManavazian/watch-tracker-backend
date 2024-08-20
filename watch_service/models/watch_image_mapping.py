from pydantic import BaseModel


class WatchImageMapping(BaseModel):
    reference_number: str
    brand: str
    image_name: str

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())