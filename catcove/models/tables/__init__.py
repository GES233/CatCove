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
    MetaData
)

metadata = MetaData()

Base = declarative_base(metadata)
