from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from uuid import UUID
from typing import List, Union

from db.models import Postcard


class PostcardDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
            self,
            image: bytearray
    ) -> Postcard:
        new_postcard = Postcard(
            image=image,
            is_liked=False
        )
        self.session.add(new_postcard)
        await self.session.commit()
        return new_postcard

    async def get_all(self) -> List[Postcard]:
        res = await self.session.execute(select(Postcard))
        return res.scalars().all()
