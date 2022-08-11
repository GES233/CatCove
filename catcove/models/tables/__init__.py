from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Boolean, String, Text, Date, DateTime, ForeignKey

try:
    from db import engine  # Absolutely import
except ImportError:
    # From the Application.
    from ...db import engine

Base = declarative_base(bind=engine)  # autocommit=False, autoflush=False

# import libs
# add `models` to sys firstly:
import os, sys
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(app_path)
from .users import Users
from .contents.posts import UserPosts
