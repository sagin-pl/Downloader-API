import sqlite3
import threading
import os
from time import sleep


def delete_file_after_5_min(name: str, uuid: str):
    sleep(300)
    db = database()
    db.deleteUUID(uuid)
    del db
    try:
        arr = name.split(',')
        if len(arr) < 2:
            os.remove("/var/www/files/" + name)
        else:
            for i in range(len(arr)):
                if i == 0:
                    arr[i] = "/var/www/files/" + arr[i].replace("'", "").replace(" ", "")[1:]
                elif i == (len(arr) - 1):
                    arr[i] = "/var/www/files/" + arr[i].replace("'", "").replace(" ", "")[:-1]
                else:
                    arr[i] = "/var/www/files/" + arr[i].replace("'", "").replace(" ", "")
                os.remove(arr[i])

    except Exception as E:
        f = open("ERORR.SAGIN.PL")
        f.write(str(E) + "\n")
        f.close()
        pass


def delete_file_after_30_sec(name: str, uuid: str):
    sleep(30)
    db = database()
    db.deleteUUID(uuid)
    del db
    try:
        os.remove("/var/www/files/" + name)
    except Exception:
        pass


class database:
    def __init__(self):
        self.connection = sqlite3.connect("./db/uuidDB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE if not exists uuid(
                                uuid TEXT PRIMARY KEY,
                                percent INTEGER NOT NULL,
                                fileName TEXT)
                            ''')
        self.connection.commit()

    def insertUUID(self, uuidT: str):
        sql = f'INSERT INTO uuid (uuid, percent) VALUES ("{uuidT}", 0)'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception as E:
            print(E)
            return False

    def updateUUID(self, uuidT: str, percent: int):
        sql = f'UPDATE uuid SET percent={percent} WHERE uuid = "{uuidT}"'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception as E:
            print("\n\n", str(E), "\n\n")
            return False

    def last_UUID_update(self, uuidT: str, fileName: str):
        sql = f'UPDATE uuid SET percent=100, fileName="{fileName}" WHERE uuid = "{uuidT}"'
        x = threading.Thread(target=delete_file_after_5_min, args=(fileName, uuidT,))
        x.start()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception:
            return False

    def downloadERROR(self, uuidT: str):
        sql = f'UPDATE uuid SET percent=-100, fileName="Bad url" WHERE uuid = "{uuidT}"'
        x = threading.Thread(target=delete_file_after_30_sec, args=(None, uuidT,))
        x.start()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception:
            return False

    def findUUID(self, uuidT: str):
        sql = f'SELECT percent FROM uuid WHERE uuid = "{uuidT}"'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            per = self.cursor.fetchone()
            if per is not None:
                return per[0]
            else:
                return -1
        except Exception as E:
            print(E)
            return -1

    def getLink(self, uuidT: str):
        sql = f'SELECT fileName FROM uuid WHERE uuid = "{uuidT}"'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            fileName = self.cursor.fetchone()
            if fileName is not None:
                return str(fileName[0])

        except Exception as E:
            print(E)
            return "Error"

    def deleteUUID(self, uuidT: str):
        sql = f'DELETE FROM uuid WHERE uuid = "{uuidT}"'
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as E:
            print(E)
            return "Error"

    def __del__(self):
        self.connection.close()
