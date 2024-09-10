from pydantic import BaseModel


class WatchImageMapping(BaseModel):
    reference_number: str
    brand: str
    image_path: str

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())