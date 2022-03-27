from requests import Session
import time
import re

from helpers.database import database


def TTDownloaderGetTiktok(uuid: str, tiktokUrl: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
                      'Safari/537.36',
        'origin': 'https://ttdownloader.com',
        'referer': 'https://ttdownloader.com/',
        'sec-ch-ua': '"Chromium";v="94",'
                     '"Google Chrome";v="94", ";'
                     'Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Linux",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        db = database()
        ses = Session()
        db.updateUUID(uuid, 5)
        init = ses.get("https://ttdownloader.com/", headers=headers)
        db.updateUUID(uuid, 15)

        token = re.findall(r'value=\"([0-9a-z]+)\"', init.text)
        db.updateUUID(uuid, 20)

        postData = {
            'url': tiktokUrl,
            'format': '',
            'token': token[0]
        }

        db.updateUUID(uuid, 40)
        r = ses.post("https://ttdownloader.com/req/", headers=headers, data=postData)
        result = r.text
        db.updateUUID(uuid, 60)

        try:
            noWatermark, watermark, audio = re.findall(
                r'(https?://.*?.php\?v\=.*?)\"', result
            )
        except Exception as E:
            return "Bad url"

        return noWatermark

    except Exception as er:
        file = open("error.szurag", 'a')
        file.write("\n\n\n\n")

        from datetime import datetime
        import pytz
        pl = pytz.timezone('Poland')
        current_time = datetime.now(pl).strftime("%H:%M:%S")

        file.write("----------TIME: {0}----------\n".format(current_time))
        file.write(str(er) + "\n")
        file.write("----------TIME: {0}----------".format(current_time))

        return "Problem"

