from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from .. import *

@declarative_mixin
class Tag(Base):
    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True
    )
    
    # status: `normal`, `hidden`, `deleted`.
    status = Column(String(16), default="normal")

    create_time = Column(DateTime, default=datetime.utcnow())

    title = Column(String(32), index=True, unique=True)
    content = Column(Text)

    thread_related = ...
    userpost_related = ...
    blog_related = ...
