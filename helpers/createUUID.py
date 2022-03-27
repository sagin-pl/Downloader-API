from helpers.database import database
import uuid


def createUUID():
    tracking = uuid.uuid4()
    db = database()
    res = db.insertUUID(tracking)
    del db
    return res
