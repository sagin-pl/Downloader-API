import uuid
from helpers.database import database


def createUUID():
    tracking = uuid.uuid4()
    db = database()
    res = db.insertUUID(tracking)
    del db
    return res, tracking
