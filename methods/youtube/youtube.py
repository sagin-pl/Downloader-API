from yt_dlp import YoutubeDL
import json
import requests
import aria2p
from helpers.database import database
import unicodedata
import re
import os

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def downloadYoutube(uuid: str, url: str, settings: str):
    def my_hook(d):
        i = 0
        if d['status'] == 'finished':
            i += 40
            db = database()
            db.updateUUID(uuid, i)
            del db

    """
    uuid: to tracking
    url: youtube link
    settings: "best" or "hd" (best can be 8k video, hd will always been 1280x720)
    """
    try:
        if settings == "best":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
                "quiet": True,
                'progress': True,
                'progress_hooks': [my_hook],
                'postprocessor-args': '-c:v libx264',
                'external_downloader': 'aria2c',
                'cookies': 'ytcook.txt',
                'recode': 'mp4',
                'playlist-items': 1,
                'external_downloader_arg': '-c -j 5 -x 10',
                'outtmpl': '/var/www/files/%(title)s.mp4'
            }
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url)
                    path = ydl.prepare_filename(info)
                    ydl.download([url])
                    Fname = slugify(path[15:-4]) + ".mp4"
                    os.rename(path, f"/var/www/files/{Fname}")
                    db = database()
                    db.last_UUID_update(uuid, Fname)
                    del db
                except Exception:
                    db = database()
                    db.downloadERROR(uuid)
                    del db

        else:
            ydl_opts2 = {
                'format': 'best',
                "quiet": True,
                'progress': True,
                'progress_hooks': [my_hook],
                'postprocessor-args': '-c:v libx264',
                'external_downloader': 'aria2c',
                'cookiefile': 'ytcook.txt',
                'recode': 'mp4',
                'playlist-items': 1,
                'external_downloader_arg': '-c -j 5 -x 10',
                'outtmpl': '/var/www/files/%(title)s.mp4'
            }
            with YoutubeDL(ydl_opts2) as ydl2:
                try:
                    info = ydl2.extract_info(url)
                    path = ydl2.prepare_filename(info)
                    ydl2.download([url])
                    Fname = slugify(path[15:-4]) + ".mp4"
                    os.rename(path, f"/var/www/files/{Fname}")
                    db = database()
                    db.last_UUID_update(uuid, Fname)
                    del db
                except Exception:
                    db = database()
                    db.downloadERROR(uuid)
                    del db


    except Exception as c:
        print("\n\n\nERROR: " + str(c) + "\n\n\n")
        pass
        return False, ""

# downloadYoutube(uuid=" ", url="https://www.youtube.com/watch?v=uKGWNdwBv8Y", settings="best")
# downloadYoutube(uuid=" ", url="https://youtu.be/LXb3EKWsInQ", settings="best")
