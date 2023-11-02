from fastapi import Depends, File

from sqlalchemy.ext.asyncio import AsyncSession

from PIL import Image, ImageDraw, ImageFont
from math import ceil

from io import BytesIO
from typing import Union, List
from uuid import UUID

from db.session import get_session
from db.dals import PostcardDAL
from schemas.postcards import PostcardPreviewData

SCREEN_SIZE = (1024, 640)
SCREEN_RATIO = SCREEN_SIZE[0] / SCREEN_SIZE[1]


def scale_and_crop_image(
        image: Image,
        required_size: list,
        required_ratio: float
):
    print("req size", required_size)
    w, h = image.size
    print("image size", image.size)
    ratio = w / h
    print("ratio", ratio)
    if ratio > required_ratio:  # long picture
        print("long")
        scale = required_size[1] / h
    else:  # high picture
        print("short")
        scale = required_size[0] / w
    print("scale", scale)
    print("new_size", required_size)
    image = image.resize(list(map(lambda x: ceil(x * scale), image.size)))
    return image.crop([0, 0, *required_size])


def get_required_params(ratio):
    required_ratio = ratio
    if required_ratio < SCREEN_RATIO:
        required_size = [
            ceil(SCREEN_SIZE[0] * (SCREEN_RATIO**(-1) / required_ratio)),
            SCREEN_SIZE[1]
        ]
    else:
        required_size = [
            SCREEN_SIZE[0],
            ceil(SCREEN_SIZE[1] * (SCREEN_RATIO / required_ratio))
        ]
    return required_size, required_ratio


class PostcardService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def save(
            self,
            file: File,
    ) -> UUID:
        postcard_dal = PostcardDAL(self.session)
        new_postcard = await postcard_dal.save(await file.read())
        return new_postcard.id

    async def get_all(self) -> List[bytearray]:
        postcard_dal = PostcardDAL(self.session)
        postcards = await postcard_dal.get_all()
        return [postcard.image for postcard in postcards]

    async def create_preview(
            self,
            file: File,
            body: PostcardPreviewData
    ):
        image = Image.open(BytesIO(await file.read()))

        required_size, required_ratio = get_required_params(body.ratio)
        image = scale_and_crop_image(image, required_size, required_ratio)
        print("scaled image size", image.size)

        draw = ImageDraw.Draw(image)

        title_font = ImageFont.truetype(f"./fonts/{body.title_font}.ttf", 76)
        title_size = title_font.getsize(body.title)
        title_pos = ((required_size[0] - title_size[0]) // 2, 5)
        draw.text(title_pos, body.title, font=title_font, fill=body.letter_color)

        if body.text_list:
            text_array = list(filter(lambda x: x, body.text_list[0].split(",")))
            print(text_array)
            text_font = ImageFont.truetype(f"./fonts/{body.text_font}.ttf", 32)
            text_size = [0, 0]
            text_size[0] = max(text_font.getsize(text)[0] for text in text_array)
            text_size[1] = text_font.getsize(text_array[0])[1]
            bottom_offset = (len(text_array) - 1) * (text_size[1]) + 5
            for text in text_array:
                text_pos = [10, required_size[1] - text_size[1] - bottom_offset]
                if body.text_align == "C":
                    text_pos[0] = (required_size[0] - text_size[0]) // 2
                elif body.text_align == "R":
                    text_pos[0] = (required_size[0] - text_size[0] - 10)
                draw.text(text_pos, text, font=text_font, fill=body.letter_color)
                bottom_offset -= text_size[1]

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
