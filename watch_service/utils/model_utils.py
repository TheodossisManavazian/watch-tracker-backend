import hashlib
from typing import Any


def dict_to_model(pkg: dict, type: Any) -> Any:
    return type(**pkg)


def obj_to_dict(obj: Any) -> dict:
    return vars(obj)


def generate_hash(val: str):
    return hashlib.sha256(val.encode("utf-8")).hexdigest()
