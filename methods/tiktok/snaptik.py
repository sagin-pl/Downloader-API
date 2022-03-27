import requests
import re
from ast import literal_eval
from helpers.decode import decoder
from helpers.database import database


def snaptikGetTiktok(uuid: str, tiktokUrl: str):
    try:
        db = database()
        db.updateUUID(uuid, 5)
        s = requests.Session()
        # token = re.findall(r'(value=)(\"([0-z]+)\")', s.get("https://snaptik.app/pl").text)[2]
        # print(token)
        req = s.post("https://snaptik.app/abc.php",
                     params={
                         'url': tiktokUrl,
                         'lang': 'pl',
                         'token': 'eyMTY0ODI5NDg5NQ==c'
                     },
                     headers={
                         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/86.0.4240.111 Safari/537.36'
                     })
        db.updateUUID(uuid, 50)
        # print(req.text)
        if "Błąd" in req.text:
            db.downloadERROR(uuid)
            del db
            return "urlissue"
        textToDecode = re.findall(r"\(\".*?,.*?,.*?,.*?,.*?.*?\)", req.text)[0]
        db.updateUUID(uuid, 55)
        decoded = decoder(*literal_eval(textToDecode))
        db.updateUUID(uuid, 60)
        link = str(re.findall(r'\"(https?://(tikcdn\.net|snapsave\.info).*?)\"', decoded)[0][0]).strip('\\')
        db.updateUUID(uuid, 70)
        del db
        return link
    except Exception as E:
        print("POBIERANIE /SZURAG --- COŚ POSZŁO NIE TAK: \n\n", str(E), "\n\n\n")
        return None
