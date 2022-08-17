from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from . import *


tag_maintainers = Table(
    # The user who can edit the tag's info.
    "tag_maintainers",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id")
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id")
    )
)

threads_tag_association = Table(
    "threads_tag_association",
    Base.metadata,
    Column(
        "thread_id",
        ForeignKey("threads.id")
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id")
    )
)

userposts_tag_association = Table(
    "userposts_tag_association",
    Base.metadata,
    Column(
        "userposts_id",
        ForeignKey("userposts.id")
    ),
    Column(
        "tag_id",
        ForeignKey("tags.id")
    )
)


class Tags(Base):
    # nutshell, tag is simpler than topic when implementating it.
    __tablename__ = "tags"

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
    description = Column(String(256), index=True)
    content = Column(Text)

    maintainers = relationship("Users", secondary=tag_maintainers, back_populates="tags")

    threads_related = relationship("Threads", secondary=threads_tag_association, back_populates="tags")
    userposts_related = relationship("UserPosts", secondary=userposts_tag_association, back_populates="tags")

    def __repr__(self) -> str:
        return "<Tag %s : %s>" % (self.id, self.title)

