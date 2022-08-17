from datetime import datetime

from .. import *

from .tags import threads_tag_association

class Threads(Base):
    __tablename__ = "threads"
    id = Column(  # id of threads.
        Integer,
        primary_key=True,
        index=True,
        unique=True)
    org_po = Column(  # OP or PO?
        Integer,
        ForeignKey("users.id")
    )
    title = Column(
        String(256),
        index=True
    )
    # `normal`, `block`, `deleted`, `hidden`
    status = Column(
        String(16)
    )
    create_time = Column(DateTime, default=datetime.utcnow())
    # parent = Column(Integer, ForeignKey("tag.id"))

    owner = relationship("Users", back_populates="threads")
    posts = relationship("PostsUnderThread", back_populates="thread")
    tags = relationship("Tags", secondary=threads_tag_association, back_populates="threads_related")

    def __repr__(self) -> str:
        return f"<Thread {self.id} by {self.org_po}>"
