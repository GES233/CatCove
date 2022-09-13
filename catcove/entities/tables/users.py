from datetime import datetime
from bcrypt import gensalt, hashpw, checkpw

from . import *

from .tags import tag_maintainers


following_table = Table(
    "following_table",
    Base.metadata,
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
    Column("followed_id", ForeignKey("users.id"), primary_key=True)
    # +-------------+   +-------------+
    # | follower_id |-->| followed_id |
    # +-------------+   +-------------+
    # Add Chinese comment:
    # 关注者（粉丝）关注了【被】关注者（关注）
    # User as a follower TO sb.
    # User followed BY sb.
)


class Users(Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        comment="The ID of user in 'users'.",
    )
    # status: `normal`, `blocked`, `freeze`, `newbie`, `deleted`
    status = Column(String(16), default="newbie")
    join_time = Column(DateTime, default=datetime.utcnow())
    nickname = Column(String(128), unique=True, nullable=False, index=True)
    username = Column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
        comment="username is ASCII only.",
    )
    email = Column(String(256), unique=True)
    password = Column(LargeBinary)
    gender = Column(String(2), nullable=True)
    birth = Column(Date, nullable=True)
    info = Column(Text, nullable=True)
    role = Column(String(16), default="user")
    # is_spectator = Column(Boolean, default=0)

    # == With other tables  == #

    """ User-to-user:

        +-------+                  +-------------+
        | Users |one <---> zero/one| User(other) |
        +-------+                  +-------------+
    """
    # role = "spectator"
    as_spectator = relationship("Spectator", uselist=False, back_populates="user")
    as_moderator = relationship("Moderator", uselist=False, back_populates="user")
    # maintainer in `tags`.

    """ Contents:
        
        +-------+                  +---------+
        | Users |one <--> zero/many| Content |
        +-------+                  +---------+
    """
    userposts = relationship("UserPosts", back_populates="owner", lazy="select")
    posts = relationship("PostsUnderThread", back_populates="owner", lazy="select")
    threads = relationship("Threads", back_populates="owner", lazy="select")
    # comments = relationship("Comments")  # I don't add here.

    """ Fields:

        +-------+                        +---------+
        | Users |zero/namy <--> zero/many|  Field  |
        +-------+                        +---------+
    """
    # Followers Following sb. ->
    # followers -> folowing
    followers = relationship(
        "Users",
        secondary=following_table,
        primaryjoin=(id == following_table.c.follower_id),
        secondaryjoin=(id == following_table.c.followed_id),
        back_populates="following",
        lazy="select",
    )
    following = relationship(
        "Users",
        secondary=following_table,
        primaryjoin=(id == following_table.c.followed_id),
        secondaryjoin=(id == following_table.c.follower_id),
        back_populates="followers",
        lazy="select",
    )
    tags = relationship(
        "Tags", secondary=tag_maintainers, back_populates="maintainers", lazy="select"
    )

    def encrypt_passwd(self, password: str) -> None:
        salt = gensalt()
        self.password = hashpw(password.encode("utf-8"), salt)

    def check_passwd(self, password: str) -> bool:
        return True if checkpw(password.encode("utf-8"), self.password) else False

    def __repr__(self) -> str:
        return "<User %s (uid:%s)>" % (self.nickname, self.id)


class Spectator(Base):
    __tablename__ = "spectator"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # 开后台用的。
    password = Column(LargeBinary)
    user = relationship("Users", uselist=False, back_populates="as_spectator")

    def encrypt_passwd(self, password: str) -> None:
        salt = gensalt(rounds=26)
        self.password = hashpw(password.encode("utf-8"), salt)

    def check_passwd(self, password: str) -> bool:
        return True if checkpw(password.encode("utf-8"), self.password) else False


class Moderator(Base):
    __tablename__ = "moderator"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", uselist=False, back_populates="as_moderator")
