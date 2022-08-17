from .. import *

from . import ContentMixin
from ..tags import threads_tag_association

class Threads(ContentMixin):
    __tablename__ = "threads"
    org_po = Column(  # OP or PO?
        Integer,
        ForeignKey("users.id")
    )
    title = Column(
        String(256),
        index=True
    )
    # parent = Column(Integer, ForeignKey("tag.id"))

    owner = relationship("Users", back_populates="threads")
    posts = relationship("PostsUnderThread", back_populates="thread")
    tags = relationship("Tags", secondary=threads_tag_association, back_populates="threads_related")

    def __repr__(self) -> str:
        return f"<Thread {self.id} by {self.org_po}>"
