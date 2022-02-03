def downloadTikTok(link):
    from yt_dlp import YoutubeDL
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from wget import download
    import os
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]',
        'postprocessor-args': '-c:v libx265',
        'outtmpl': './temp/tik/%(title)s.%(ext)s'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link)
        # print(info)
        plik = ydl.prepare_filename(info)
        ydl.download([link])
        driver = webdriver.Chrome()
        driver.get("https://www.onlineconverter.com/hevc-to-mp4")
        driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(os.getcwd() + "/" + plik)
        driver.find_element(By.XPATH, '//input[@type="button"]').click()
        wait = WebDriverWait(driver, 30)
        link = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@onclick, "return canDownload();")]'))).get_attribute("href")
        path = "./" + plik
        os.remove(path)
        download(link, path)

downloadTikTok("https://www.tiktok.com/@bodi__4ka/video/7069733264654748933")