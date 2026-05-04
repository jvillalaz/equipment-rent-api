from datetime import datetime, timezone
from typing import Any

from bson.objectid import ObjectId
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

def naive_utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def to_naive_utc(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

def to_camel_without_underscore(v: str):
    camel = to_camel(v)
    return camel.replace("_", "")


def exclude_empty_lists(model_dict):
    return {key: value for key, value in model_dict.items() if not (isinstance(value, (list, dict)) and not value)}


class DTO(BaseModel):
    model_config = ConfigDict(
        strict=False,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        alias_generator=to_camel_without_underscore,
        json_encoders={
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
            ObjectId: lambda v: str(v),
        },
    )

    def model_dump(self, exclude_none=False, **kwargs) -> dict[str, Any]:
        data = super().model_dump(**kwargs)
        if exclude_none:
            return exclude_empty_lists(data)

        return data

    def __init__(self, **attrs):
        if '_id' in attrs and isinstance(attrs['_id'], ObjectId):
            attrs['_id'] = str(attrs['_id'])
        super().__init__(**attrs)


class MetaService(type):

    def __new__(mcs, *args, **kwargs):

        new_class = super().__new__(mcs, *args, **kwargs)
        for property_name in new_class.__dict__:
            property_value = getattr(new_class, property_name)

            if callable(property_value):
                if hasattr(property_value, "__func__"):
                    setattr(property_value.__func__, "_doc_exceptions", "")
                else:
                    setattr(property_value, "_doc_exceptions", "")

        return new_class


class Service(metaclass=MetaService):
    pass
