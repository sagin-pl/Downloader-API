from flask import Flask
from flask import jsonify
from flask import request
import bcrypt
from downloadTT import *
from downloadIG import *

haslo = u"-. .. --. --. . .-."
bazaURL = "http://34.116.192.77:2115/"

app = Flask(__name__)

@app.route('/czy_oddycha', methods=['GET'])
def czy_oddycha():
    return jsonify(api_zyje='API oddycha!')

def auth(hash):
    try:
        if bcrypt.checkpw(haslo.encode('utf-8'), hash.encode('utf-8')):
            print("HASLO SIE ZGADZA")
            return True
        else:
            print("Blad uwierzytelniania")
            return False
    except Exception as e:
        return "Error"

@app.route('/v', methods=['POST'])
def auto():
    request_data = request.get_json()
    authReturn = auth(request_data['hash'])
    if authReturn:
        sciezka = ''
        platforma = request_data['platform']
        url = request_data['url']
        platformy = [
            'tt',
            'yt',
            'ig',
            'ph'
        ]
        if platforma == platformy[0]:
            if request_data['audio'] == 0:
                download, path = PobierzTT(url)
                if download == True and path != "":
                    sciezka = bazaURL + str(path)[1:]
            else:
                download, path = PobierzTTAudio(url)
                if download == True and path != "":
                    sciezka = bazaURL + str(path)[1:]
        elif platforma == platformy[2]:
            #download, path = pobierzIG(url)
            #if download and path != "":
                #sciezka = bazaURL + path
            pass




        return jsonify(url=sciezka)
    else:
        return "Wywal error"


if __name__ == '__main__':
    app.run(port=2137, debug=True, host='0.0.0.0')
