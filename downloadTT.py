from yt_dlp import YoutubeDL

def PobierzTT(link):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/mp4',
            'postprocessor-args': '-c:v libx264',
            'use-postprocessor': 'ffmpeg',
            'merge-output-format': 'mp4',
            'verbose': True,
            'outtmpl': './temp/tik/%(id)s.mp4'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link)
            # print(info)
            plik = "/" + str(ydl.prepare_filename(info).replace("\\", "/"))
            ydl.download([link])
            plik = plik[6:]
        return True, plik

def PobierzTTAudio(link):
    try:
        print("POBIERANIE AUDIO")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '384',
            }],
            'outtmpl': './temp/tik/%(id)s.mp3'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link)
            # print(info)
            path = ydl.prepare_filename(info)
            ydl.download([link])
            path = path[6:]
        return True, path
    except Exception:
        pass
        return False, ""