from .extensions import db
from .models import User

def seed_database():
    if User.query.first():
        return

    vendor = User(username="")
