# Downloader API
[![Release](https://img.shields.io/github/v/release/sagin-pl/downloader-api)](https://github.com/sagin-pl/Downloader-API/releases)
[![Project](https://img.shields.io/badge/project-SAGIN--PL-green)](https://github.com/sagin-pl)

Downloader API to interfejs, który ułatwia pracę innych programistów. Dzięki API unikamy wielu powtórzeń w kodzie na każdą platformę. Downloader pozwala na pobiranie filmów i zdjęć z popularnych platform takich jak Instagram, TikTok, Youtube. Framework, który został użyty to FastAPI.

## SPIS TREŚCI
- [Wymagania](#wymagania)
- [Funkcje](#funkcje)
- [Użycie](#użycie)
- [Changelog](#changelog)


## WYMAGANIA
- Internet
- Podstawowe pojęcie jak korzystać z różnego rodzaju API

## FUNKCJE
- Pobieranie TikToków
- Pobieranie zdjęć i filmów z Instagrama
- Pobieranie filmów z YouTube

## Użycie

Wysyłamy requesta na adres zgodnie z naszymi potrzebami:

#### TikTok i Instagram 
```https://api.sagin.pl/szurag```

Po wykonaniu requesta metodą POST otrzymujemy odpowiedź JSON
```json
{
  "url": "https://api.sagin.pl/track/5fe15dc6-bc0b-4334-8af3-09ef69903d2e"
}
```

Do otrzymanego linku wykonujemy zapytanie GET na adres URL otrzymany z poprzedniego requesta.
Przykładowa odpowiedź jaką otrzymamy po zakończeniu pobierania filmu na serwer:

```json
{
  "5fe15dc6-bc0b-4334-8af3-09ef69903d2e": "https://files.sagin.pl/7089476830431841538.mp4",
}
```

**Jeżeli film pobiera się dłużej to wtedy otrzymamy wersję z procentami w liczbie całkowitej (INT): **
```json
{
  "5fe15dc6-bc0b-4334-8af3-09ef69903d2e": 40
}
```
Po otrzymaniu finalnej odpowiedzi z URL'em do pobrania filmu z serwera, możemy go zapisać.
\*Nigdy nie zobaczymy procentów w wartości 100, ponieważ przy spełnieniu warunki (if procenty == 100) zamienia się na URL.


#### YouTube
```https://api.sagin.pl/szuragV2```

YouTube wymaga argument więcej:
best oznacza najlepszą dostępną jakość z jaką zostanie zwrócony film

- "settings": "best"
**lub**
- "settings": "hd"

```json
{
  "url": "https://www.youtube.com/watch?v=e4n15OGWzEk",
  "settings": "best"
}
```

Po wykonaniu requesta metodą POST otrzymujemy odpowiedź JSON
```json
{
  "url": "https://api.sagin.pl/track/5fe15dc6-bc0b-4334-8af3-09ef69903d2e"
}
```

Do otrzymanego linku wykonujemy zapytanie GET na adres URL otrzymany z poprzedniego requesta.
Przykładowa odpowiedź jaką otrzymamy po zakończeniu pobierania filmu na serwer:

```json
{
  "5fe15dc6-bc0b-4334-8af3-09ef69903d2e": "https://files.sagin.pl/7089476830431841538.mp4",
}
```

**Jeżeli film pobiera się dłużej to wtedy otrzymamy wersję z procentami w liczbie całkowitej (INT): **
```json
{
  "5fe15dc6-bc0b-4334-8af3-09ef69903d2e": 40
}
```
Po otrzymaniu finalnej odpowiedzi z URL'em do pobrania filmu z serwera, możemy go zapisać.
\*Nigdy nie zobaczymy procentów w wartości 100, ponieważ przy spełnieniu warunki (if procenty == 100) zamienia się na URL.



# Changelog


### ALPHA
- 02.02.2022 - Możliwość sprawdzenia czy (API) jest dostępne, pobieranie filmu z TikToka bez znaku wodnego platformy, możliwość pobrania samego dźwięku z filmu
- 03.02.2022 - API sprawdza czy “hash” się zgadza z hasłem

### BETA
- 13.03.2022 - <span style="color:red">FATALNY BŁĄD API (trzeba przepisać kod)</span>


### RELEASE
- 29.03.2022 Przepisanie oraz naprwawienie kodu. API działa. Odejście z koncepcji zabezpieczania API.

## Autor
- [Szurag](https://github.com/thebartle)
