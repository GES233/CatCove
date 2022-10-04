from sqlalchemy.sql import select, update, or_, insert
from sqlalchemy.orm import sessionmaker


from . import ServiceBase
from ..entities.tables.contents.posts import (
    UserPosts,
    PostsUnderThread,
)
from ..entities.tables.users import Users


class UserPostsService(ServiceBase):
    def __init__(
        self,
        db_session: sessionmaker,
    ) -> None:
        ...
