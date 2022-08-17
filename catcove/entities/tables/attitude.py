from typing import Tuple
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.types import DECIMAL
from datetime import datetime

from . import *


@declarative_mixin
class AtittudeBase(Base):
    """ How `User.Attitude -> Content`?
        
        larger than assistance table.

        +------+            +---------+
        | User |many<-->many| Content |
        +------+            +---------+

                    ||
                    \/
        
        +---------------+
        |    Attitude   |
        +---------------+
        |  holder_id FP |-->Users.id
        +---------------+
        | content_id FP |-->Content.id
        +---------------+
        | ....
        | thumb, angry, etc.
        +---------------+
    """
    __abstract__ = True
    # => 2 Primary Key.

    @declared_attr
    def holder_id(self) -> Column:
        return Column(
            Integer,
            ForeignKey("users.id"),
            primary_key=True
        )
    
    # And a terget_id as a primary key.

    set_time = Column(DateTime, default=datetime.utcnow())

    # I wanna use PAD model to take convience for
    # comming emotional analyse.
    pleasure = Column(DECIMAL(precision="8, 7"), nullable=False)
    arousal = Column(DECIMAL(precision="8, 7"), nullable=False)
    dominance = Column(DECIMAL(precision="8, 7"), nullable=False)

    @declared_attr
    def get_attitude(self) -> Tuple:
        return (eval(self.pleasure), eval(self.arousal), eval(self.dominance))

    # Add some decorator?
    def set_attitude(self, P: float, A: float, D: float) -> Tuple:
        self.pleasure = P
        self.arousal = A
        self.dominance = D
        return self.get_attitude


class AttitudeForUserPosts(AtittudeBase):
    __tablename__ = "attitude_for_userposts"

    userpost_id = relationship()

