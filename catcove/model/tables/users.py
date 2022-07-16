from datetime import datetime
from bcrypt import gensalt, hashpw, checkpw

from . import *


class Users(Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        comment="The ID of user in 'users'."
    )
    # status: `normal`, `blocked`, `freeze`, `newbie`, `deleted`
    status = Column(String(16), default="newbie")
    join_time = Column(DateTime, default=datetime.utcnow())
    nickname = Column(
        String(128),
        unique=True,
        index=True
    )
    username = Column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
        comment="username is ASCII only."
    )
    email = Column(String(256), unique=True)
    password = Column(String)
    gender = Column(String(2), nullable=True)
    birth = Column(Date, nullable=True)
    info = Column(Text, nullable=True)
    is_spectator = Column(Boolean, default=0)

    # == With other tables  == #

    """ Contents:
        
        +-------+                 +---------+
        | Users |one --> zero/many| Content |
        +-------+                 +---------+
    """
    userposts = relationship("UserPosts", back_populates="owner")
    # posts = relationship("Posts")
    # comments = relationship("Comments")  # I don't add here.

    def encrypt_passwd(self, password: str) -> None:
        salt = gensalt()
        self.password = hashpw(password.encode("utf-8"), salt)
    
    def check_passwd(self, password: str) -> bool:
        return True if checkpw(password.encode("utf-8"), self.passwd) else False

    def __repr__(self) -> str:
        return 'User %s (uid:%d)' %(self.nickname, self.id)
