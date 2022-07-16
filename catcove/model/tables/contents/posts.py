from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from .. import *

@declarative_mixin
class Posts(Base):
    __abstract__ = True

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True
    )
    @declared_attr
    def owner_id(self):
        return Column(
            Integer,
            ForeignKey("users.id"))
    # status: `normal`, `hidden`, `deleted`.
    status = Column(String(16), default="normal")
    create_time = Column(DateTime, default=datetime.utcnow())
    content = Column(Text)

    @declared_attr
    def __repr__(self) -> str:
        return '<Post %s from %s at %s>' % (
            self.id,
            self.owner_id,
            self.create_time
        )


class PostsUnderThread():  # Remove heritage.
    __tablename__ = "posts"

    parent = Column(Integer, ForeignKey("threads.id"))
    loc = Column(
        Integer,
        comment="loc(location), i.e. index in thread."
    )


class UserPosts(Posts):
    __tablename__ = "userposts"
    owner = relationship("Users", back_populates="userposts")
