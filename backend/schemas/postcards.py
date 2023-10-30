from typing import List
from uuid import UUID

import binascii
from pydantic import BaseModel, Field, field_validator


class TunedModel(BaseModel):

    class Config:
        from_attributes = True


class ByteA:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, bytes):
            raise ValueError(f'`bytes` expected not {type(v)}')
        return binascii.b2a_hex(v)


class PostcardSaving(BaseModel):
    image: bytes


class PostcardPreviewData(BaseModel):
    title: str
    title_font: str
    text_list: List[str]
    text_font: str
    text_align: str = Field(r"^(R|L|C)$")
    letter_color: str = "black"
    ratio: float

    @field_validator('text_list')
    def validate_string_list_length(cls, value):
        if len(value) > 5:
            raise ValueError("Список строк не может содержать более 5 элементов")
        return value
