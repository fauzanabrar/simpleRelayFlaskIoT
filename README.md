# Simulasi Relay IoT dengan Restful API di Wokwik

Mengendalikan alat IoT dengan request ke Restful API 
untuk mengontrol relay pada microcontroller ESP32 dengan 
micropython. Simulasinya bisa di run di [wokwi](https://wokwi.com)
dan aplikasi RESTfulnya dibuat dengan Flask.

## Feature
- On/Off relay
- timer
- scheduler cronjob

## Installation
Deploy FlaskApp di public server, alternatif bisa gunakan
[Replit](https://replit.com). Kemudian install requirementnya
terlebih dahulu.

```
 pip install -r requirements.txt
```
Jalankan FlaskApp
```
flask --app main run
```
Copy code di IoT.py dan paste di [wokwi](https://wokwi.com) 
kemudian ubah url nya dengan aplikasi flask yang sudah 
dijalankan tadi.

