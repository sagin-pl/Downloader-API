import re
from random import randint

def VideoID(url: str):
    try:
        ID = re.findall(r"(@[a-zA-z0-9]*|.*)(\/.*\/|trending.?shareId=)([\d]*)", url)
        if not len(str(ID[0][-1])) > 0:
            return str(randint(1,100000000))
        return str(ID[0][-1])
   
    except Exception:
        return False
