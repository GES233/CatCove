from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from . import *


tag_maintainers = Table(
    # The user who can edit the tag's info.
    "tag_maintainers",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("tag_id", ForeignKey("tags.id"), nullable=False),
)

threads_tag_association = Table(
    "threads_tag_association",
    Base.metadata,
    Column("thread_id", ForeignKey("threads.id"), nullable=False),
    Column("tag_id", ForeignKey("tags.id"), nullable=False),
)

userposts_tag_association = Table(
    "userposts_tag_association",
    Base.metadata,
    Column("userposts_id", ForeignKey("userposts.id"), nullable=False),
    Column("tag_id", ForeignKey("tags.id"), nullable=False),
)


class Tags(Base):
    # nutshell, tag is simpler than topic when implementating it.
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    # status: `normal`, `hidden`, `deleted`.
    status = Column(String(16), default="normal", nullable=False)

    create_time = Column(DateTime, default=datetime.utcnow())

    title = Column(String(32), index=True, unique=True, nullable=False)
    description = Column(String(1024), index=True, nullable=True)
    content = Column(Text, nullable=True)

    maintainers = relationship(
        "Users", secondary=tag_maintainers, back_populates="tags", lazy="select"
    )

    threads_related = relationship(
        "Threads",
        secondary=threads_tag_association,
        back_populates="tags",
        lazy="select",
    )
    userposts_related = relationship(
        "UserPosts",
        secondary=userposts_tag_association,
        back_populates="tags",
        lazy="select",
    )

    def __repr__(self) -> str:
        return "<Tag %s : %s>" % (self.id, self.title)
