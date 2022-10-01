from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from . import *


class CollectSets(Base):
    __tablename__ = "collect_sets"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        comment="The ID of set.",
    )
    create_at = Column(
        DateTime,
        default=datetime.utcnow(),
    )
    name = Column(
        String(64),
        nullable=False,
        index=True,
        comment="The name of set.",
    )
    description = Column(String(1024))

    owner_id = Column(ForeignKey("users.id"))
    # owner = relationship()

    # 属性
    invisable = Column(
        Boolean,
        nullable=False,
    )

    # 和各个元素的关系
    # 这部分就硬删除了，和核心业务没啥关系
    ...

    def __repr__(self) -> str:
        return "<CollectSets '{}' for user {}>".format(self.name, self.owner_id)


@declarative_mixin
class CollectItems(Base):
    __abstract__ = True
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
    )
    collect_time = Column(
        DateTime,
        default=datetime.utcnow(),
    )
    set_id = Column(ForeignKey("collect_sets.id"))

    # `item_id` in sub-class.
    """
    @declared_attr
    def belongs_to(self):
        return relationship("CollectSets")"""
    ...


class CollectedThread(CollectItems):
    __tablename__ = ""

    thread_id = Column(ForeignKey("thread.id"))
    belongs_to = relationship("CollectSets")

    def __repr__(self) -> str:
        ...


# UserPosts
# Tag
