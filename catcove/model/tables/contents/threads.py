from .. import *
from datetime import datetime

class Threads(Base):
    __tablename__ = "threads"
    id = Column(  # id of threads.
        Integer,
        primary_key=True,
        index=True)
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
    # parent = Column(Integer, ForeignKey("group.id"))

    def __repr__(self) -> str:
        return f"<Thread {self.id} by {self.op}>"
