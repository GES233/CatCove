from sqlalchemy.orm import declarative_mixin

from . import *


class CollectSets(Base):
    __tablename__ = "collect_sets"
    ...


@declarative_mixin
class CoolectItems(Base):
    __abstract__ = True
    ...


# Thread(as index)
# UserPosts
# Tag
