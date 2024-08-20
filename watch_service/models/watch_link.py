from pydantic import BaseModel


class WatchLink(BaseModel):
    reference_number: str
    brand: str
    links: dict

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())