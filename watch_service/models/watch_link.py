from pydantic import BaseModel


class WatchLink(BaseModel):
    reference_number: str
    brand: str
    links: dict
    watch_link: str | None
    image_link: str | None

    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())