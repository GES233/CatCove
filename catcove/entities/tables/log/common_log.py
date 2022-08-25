from .. import *
from sqlalchemy import Index
from datetime import datetime

""" Common log:
    
    To storge any oprations by user.

    ========

    Using unique database.
"""
class Logs(Base):
    __tablename__ = "logs"
    
    # It's only set SUCCESS operaton.
    
    id = Column(
        Integer,
        primary_key=True
    )
    operator_id = Column(
        Integer(),
        ForeignKey("users.id")
    )
    operation_method = Column(
        String(4)
    )
    # 2 letters:
    # - C_: Create.
    # - R_: Read.
    # - U_: Update.
    # - D_: Delete.
    # - A_: Access(login/online).
    # - U_: Unaccess(logout/offline).
    # - _O: by Owner.
    # - _S: by Spectator.
    # - _M: by Moderator.
    # - _A: by Application.
    terget_user_id = Column(
        Integer(),
        ForeignKey("users.id")
    )
    target_type = Column(
        String()
    )  # Table name.
    target_id = Column(
        String()
    )
    operation_time = Column(
        DateTime(),
        default=datetime.utcnow()
    )
    content = Column(
        Text()
    )
    comment = Column(
        String()
    )
    # relationship
    operator = relationship(
        "Users", back_populates="log_operator",
        lazy="select"
        # if `oprator` == None --> App's operation.
    )
    target_user = relationship(
        "Users", back_populates="log_targer",
        lazy="select"
    )

    __table_args__ = (
        Index("idx_logs_target_type_target_id", "target_type", "target_id"),
    )
