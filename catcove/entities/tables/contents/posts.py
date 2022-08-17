from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from .. import *

from . import ContentMixin
from ..tags import userposts_tag_association

@declarative_mixin
class Posts(ContentMixin):
    __abstract__ = True

    @declared_attr
    def owner_id(self):
        return Column(
            Integer,
            ForeignKey("users.id"))

    content = Column(Text)

    @declared_attr
    def __repr__(self) -> str:
        return '<Post %s from %s at %s>' % (
            self.id,
            self.owner_id,
            self.create_time
        )


class PostsUnderThread(Posts):  # Remove heritage.
    __tablename__ = "posts"

    parent = Column(Integer, ForeignKey("threads.id"))
    owner = relationship("Users", back_populates="posts")
    thread = relationship("Threads", back_populates="posts")
    loc = Column(
        Integer,
        comment="loc(location), i.e. index in thread."
    )


class UserPosts(Posts):
    __tablename__ = "userposts"
    
    owner = relationship("Users", back_populates="userposts")

    tags = relationship("Tags", secondary=userposts_tag_association, back_populates="userposts_related")
