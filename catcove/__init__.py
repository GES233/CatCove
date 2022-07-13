import os, sys

app_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(app_path)

from app import create_app
