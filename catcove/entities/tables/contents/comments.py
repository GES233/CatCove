from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr

from .. import *

@declarative_mixin
class CommentsBase(Base):
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
    
    # locate.
    lgt = Column(Integer)
    rgt = Column(Integer)
    depth = Column(Integer)

    # Query:
    # SELECT * FROM `comments`
    # WHERE (
    #     SELECT `comments.lgt`, `comments.rgt`, `comments.depth` FROM `comments`
    #     WHERE `comments.parent_id` = ?
    # );
    # ====
    # Add:
    # UPDATE `comments`
    # SET lgt = 
    #     CASE 
    #         WHEN lgt >= $parent_node.rgt
    #             THEN lgt = lgt + 2
    #         ELSE lgt
    #     END,
    #     rgt = rgt + 2 WHERE rgt >= $parent_node.lgt;
    # INSERT INTO comments ... WHERE VALUES (...)
    # $lgt = $parent.lgt + 1; $rgt = $lgt + 1; $depth = $parent_node.path + 1
    # ====
    # Update: だめ
    # ====
    # Delete: status = "delete"

    # status: `normal`, `hidden`, `deleted`.
    status = Column(String(16), default="normal")

    create_time = Column(DateTime, default=datetime.utcnow())

    content = Column(Text)

    @declared_attr
    def __repr__(self) -> str:
        return '<Comment %s from %s at %s>' % (
            self.id,
            self.owner_id,
            self.create_time
        )


class CommentsUnderUserPosts(CommentsBase):
    __tablename__ = "comments_under_userposts"
    parent_node = Column(
        Integer,
        ForeignKey("userposts.id")
    )
    ...


class CommentsUnderPosts(CommentsBase):
    __tablename__ = "comments_under_posts"
    parent_node = Column(
        Integer,
        ForeignKey("posts.id")
    )
    ...

