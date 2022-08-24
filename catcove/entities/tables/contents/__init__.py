from .. import *
from datetime import datetime
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class ContentMixin(Base):
    __abstract__ = True
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True
    )
    # `normal`, `block`, `deleted`, `hidden`
    status = Column(
        String(16)
    )
    create_time = Column(DateTime, default=datetime.utcnow())

    content = Column(Text)