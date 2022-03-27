import json
import shutil

import requests

from helpers.database import database
import instaloader
from instaloader import Post
import re


def init():
    global L
    L = instaloader.Instaloader(compress_json=False,
                                filename_pattern="{shortcode}",
                                save_metadata=True,
                                dirname_pattern="/var/www/files/{shortcode}",
                                download_video_thumbnails=False,
                                quiet=True,
                                download_pictures=False,
                                download_videos=False)
    try:
        L.load_session_from_file("")
    except Exception as e:
        print(e)
        L.login("", "")
        L.save_session_to_file()


def getInstagram(uuid: str, igUrl: str):
    db = database()
    try:
        init()
        db.updateUUID(uuid, 1)

        short = re.findall(r'([\w-]+)\/?(\?.*)?$', igUrl)[0][0]
        path = f"/var/www/files/{short}"
        post = Post.from_shortcode(L.context, short)
        L.download_post(post, f"{short}")
        db.updateUUID(uuid, 15)

        f = open(f"/var/www/files/{short}/{short}.json")
        data = json.load(f)
        f.close()
        shutil.rmtree(f"/var/www/files/{short}")
        db.updateUUID(uuid, 25)
        if post.is_video:
            db.updateUUID(uuid, 50)
            del db
            return data['node']['video_url'], "1video", short
        else:
            if data['node']['__typename'] == "GraphSidecar":
                List = []
                photos = data['node']['edge_sidecar_to_children']['edges']
                for photo in photos:
                    List.append(photo['node']['display_resources'][-1]['src'])
                db.updateUUID(uuid, 50)
                del db
                return List, "Xphoto", short
            else:
                photo = data['node']['display_resources'][-1]['src']
                db.updateUUID(uuid, 50)
                del db
                return photo, "1photo", short


    except Exception as E:
        db.downloadERROR(uuid)
        print(E)
        del db
        pass

def downloadInstagram(uuid: str, igUrl: str):
    toDownload, Type, short = getInstagram(uuid, igUrl)
    local_filename = short

    if Type == "1video" or Type == "1photo":
        if Type == "1video":
            local_filename = local_filename + ".mp4"
        else:
            local_filename = local_filename + ".jpg"

        db = database()
        try:
            path = "/var/www/files/" + local_filename
            with requests.get(toDownload, stream=True) as r:
                r.raise_for_status()
                file_total_size = int(r.headers.get('Content-Length'))
                file_1_10 = file_total_size / 10
                downloaded = 0
                i = 50
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=4096):
                        downloaded += len(chunk)
                        if downloaded >= file_1_10:
                            i += 5
                            db.updateUUID(uuid, i)
                            file_1_10 += file_total_size / 10
                        f.write(chunk)
                db.last_UUID_update(uuid, local_filename)
                del db
        except Exception as E:
            print(E)
            db.downloadERROR(uuid)
            del db

    else:
        db = database()
        i = 1
        j = 50
        List = []
        length = len(toDownload)
        local_filename = local_filename + ".jpg"
        for url in toDownload:
            path = "/var/www/files/" + str(i) + local_filename

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                downloaded = 0
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=4096):
                        downloaded += len(chunk)
                        f.write(chunk)
                j += int(50 / length)
                db.updateUUID(uuid, j)
                List.append(str(i) + local_filename)

            i += 1
        db.last_UUID_update(uuid, str(List))
        del db
