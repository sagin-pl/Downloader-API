import os
from methods.tiktok.snaptik import snaptikGetTiktok
from methods.tiktok.TTDownloader import TTDownloaderGetTiktok
import requests
import time
from helpers.getTikTokVideoID import VideoID
from helpers.database import database


def downloadToSagin(uuid: str, tiktokUrl: str):
    link = snaptikGetTiktok(uuid, tiktokUrl)
    if link == "urlissue":
        return "bad url", None
    elif link is None:
        link = TTDownloaderGetTiktok(uuid, tiktokUrl)

    db = database()
    local_filename = VideoID(tiktokUrl) + ".mp4"
    path = "/var/www/files/" + local_filename
    with requests.get(link, stream=True) as r:
        r.raise_for_status()
        file_total_size = int(r.headers.get('Content-Length'))
        file_1_10 = file_total_size / 10
        downloaded = 0
        i = 70
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                downloaded += len(chunk)
                if downloaded >= file_1_10:
                    i += 3
                    db.updateUUID(uuid, i)
                    file_1_10 += file_total_size / 10
                f.write(chunk)
        db.last_UUID_update(uuid, local_filename)
        del db

    return path, local_filename

# downloadToSaginSnaptik("https://www.tiktok.com/@gnizdo.dk/video/7063759337214184709")
