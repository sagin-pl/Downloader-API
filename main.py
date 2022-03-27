import re

import aioredis
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel

from helpers.createTracking import createUUID
from helpers.limiter import FastAPILimiter
from helpers.limiter.depends import RateLimiter
from methods.instagram.instagram import downloadInstagram
from methods.tiktok.saveOnSagin import downloadToSagin
from methods.youtube.youtube import downloadYoutube
from helpers.database import database


class Post(BaseModel):
    url: str


class Postv2(BaseModel):
    settings: str
    url: str


app = FastAPI(
    title="Downloader Szurag",
    description="Szurag to kox",
    version="0.0.5",
    contact={
        "name": "Szurag",
        "url": "https://sagin.pl/contact/"
    }
)


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)


@app.get("/v1", dependencies=[Depends(RateLimiter(times=2, seconds=5))], description="Zwraca tylko czy api oddycha")
async def oddycha():
    return {"Mordo": "ApiOddycha"}


@app.post("/szurag", dependencies=[Depends(RateLimiter(times=1, seconds=5))], description="Na razie tylko url jest istotne reszta musi byc ale nie prawdziwa")
async def tikIG(dane: Post, background_tasks: BackgroundTasks):
    print(dane)
    if "tiktok" in dane.url:
        res, tracking = createUUID()
        if res:
            background_tasks.add_task(downloadToSagin, uuid=tracking, tiktokUrl=dane.url)
            return {'url': "https://api.sagin.pl/track/" + str(tracking)}
        else:
            return HTTPException(status_code=503)
    elif "instagram" in dane.url:
        pass
        res, tracking = createUUID()

        if res:
            background_tasks.add_task(downloadInstagram, uuid=tracking, igUrl=dane.url)
            return {'url': "https://api.sagin.pl/track/" + str(tracking)}
    else:
        return {"Mordo": "Zły url"}


@app.post("/szuragV2", dependencies=[Depends(RateLimiter(times=3, seconds=60))], description="Na razie tylko url i settings (przyjmuje tylko best i hd) reszta musi byc ale nie prawdziwa")
async def ytAndOther(dane: Postv2, background_tasks: BackgroundTasks):
    print(dane)
    if "youtu" in dane.url or "pornhub" in dane.url:
        if "&" in dane.url:
            dane.url = dane.url.split("&")[0]
        res, tracking = createUUID()
        if res:
            # downloadYoutube(uuid=" ", url="https://www.youtube.com/watch?v=uKGWNdwBv8Y", settings="best")
            background_tasks.add_task(downloadYoutube, uuid=tracking, url=dane.url, settings=dane.settings)
            return {'url': "https://api.sagin.pl/track/" + str(tracking)}
        else:
            return HTTPException(status_code=503)

    else:
        return {"Mordo": "Zły url"}


@app.get("/track/{uuid}", dependencies=[Depends(RateLimiter(times=20, seconds=5))], description="Zwraca status danego uuid")
async def track(uuid: str, background_tasks: BackgroundTasks):
    if len(uuid) == 36:
        db = database()
        perc = db.findUUID(uuid)

        if perc == 100:
            link = db.getLink(uuid)
            arr = link.split(',')
            if len(arr) < 2:
                link = "https://files.sagin.pl/" + link
                return {uuid: link}
            else:
                for i in range(len(arr)):
                    if i == 0:
                        arr[i] = "https://files.sagin.pl/" + arr[i].replace("'", "").replace(" ", "")[1:]
                    elif i == (len(arr) - 1):
                        arr[i] = "https://files.sagin.pl/" + arr[i].replace("'", "").replace(" ", "")[:-1]
                    else:
                        arr[i] = "https://files.sagin.pl/" + arr[i].replace("'", "").replace(" ", "")
                return {uuid: arr}

        elif perc >= 0:
            return {uuid: perc}
        elif perc == -100:
            raise HTTPException(status_code=200, detail="Bad URL, uuid is good")
        else:
            del db  # dla bezpieczeństwa
            raise HTTPException(status_code=404, detail="UUID not found")


    else:
        raise HTTPException(status_code=404, detail="Item not found")


##########################################################################################################################################################################


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=2137)
