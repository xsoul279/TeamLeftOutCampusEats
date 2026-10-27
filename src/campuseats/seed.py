from .extensions import db
from .models import User

def seed_database():
    if User.query.first():
        return

    vendor = User(username="Flat Top Grill", email="flattopgrill@msudenver.edu", role="vendor")
    vendor.set_password("grilled_cheese8")
    student = User(username="Lucky Guy", email="identityv@msudenver.edu", role="student")
    student.set_password("luckisAskill2")
    db.session.add(vendor)
    db.session.add(student)
    db.session.commit()
