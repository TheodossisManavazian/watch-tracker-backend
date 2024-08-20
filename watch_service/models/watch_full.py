from pydantic import BaseModel
from watch_service.models.watch import Watch
from watch_service.models.watch_image_mapping import WatchImageMapping
from watch_service.models.caliber import Caliber


class WatchFull(BaseModel):
    watch: Watch
    image_mapping: WatchImageMapping
    caliber: Caliber
    
    def __str__(self) -> str:
        return "\n".join("%s: %s" % item for item in vars(self).items())
