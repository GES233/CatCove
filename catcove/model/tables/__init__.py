from sqlalchemy.orm import declarative_base
from db import engine_bind  # Absolutely import

from sqlalchemy import Column, Integer, Boolean, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base(bind=engine_bind)  # autocommit=False, autoflush=False

# import libs
# add `models` to sys firstly:
import os, sys
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(app_path)
from .users import Users
