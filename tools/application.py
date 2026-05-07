from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, model_serializer
from pydantic.alias_generators import to_camel


def naive_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def to_camel_without_underscore(v: str) -> str:
    return to_camel(v).replace("_", "")


def exclude_empty_collections(model_dict: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in model_dict.items() if not (isinstance(v, (list, dict)) and not v)}


class DTO(BaseModel):
    model_config = ConfigDict(
        strict=False,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        alias_generator=to_camel_without_underscore,
    )

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> dict[str, Any]:
        data = handler(self)
        return {
            k: v.isoformat().replace("+00:00", "Z") if isinstance(v, datetime) else v
            for k, v in data.items()
        }

    def model_dump(self, exclude_empty: bool = False, **kwargs) -> dict[str, Any]:
        data = super().model_dump(**kwargs)
        if exclude_empty:
            return exclude_empty_collections(data)
        return data


class Service:
    pass
