from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    MetaData,
    Table,
    LargeBinary,
)

metadata = MetaData()

Base = declarative_base(metadata)

from .users import Users, following_table
from .contents.posts import UserPosts, PostsUnderThread
from .contents.threads import Threads
from .tags import (
    Tags,
    tag_maintainers,
    threads_tag_association,
    userposts_tag_association,
)
