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
    Table
)

metadata = MetaData()

Base = declarative_base(metadata)

from .users import Users
from .contents.posts import UserPosts, Posts, PostsUnderThread
from .contents.threads import Threads
from .contents.tags import Tags, tag_maintainers, threads_tag_association, userposts_tag_association
