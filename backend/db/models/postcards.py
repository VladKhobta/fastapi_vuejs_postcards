from .base import Base

from sqlalchemy import Column, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Postcard(Base):

    __tablename__ = "postcards"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    image = Column(
        LargeBinary
    )
    is_liked = Column(
        Boolean,
        unique=False,
        default=False
    )
