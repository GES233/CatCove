from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Boolean, String, Text, Date, DateTime, ForeignKey

# import libs
# add `tables` to sys firstly:
import sys
from pathlib import Path
prj_path = Path(__file__).cwd().__str__()
sys.path.append(prj_path)

try:
    try:
        # From the Application.
        from ...db import engine
    except ImportError:
        # Absolutely import
        from db import engine
except ModuleNotFoundError:
    raise Exception("Please running server from app.py!")

Base = declarative_base(bind=engine)  # autocommit=False, autoflush=False


from .users import Users
from .contents.posts import UserPosts
