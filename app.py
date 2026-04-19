import os
from flask import Flask, send_from_directory
from flask_sock import Sock
import json
from pymongo import MongoClient
from datetime import datetime
from google.cloud import pubsub_v1

if "GOOGLE_JSON" in os.environ:
    with open("bulut-anahtar.json", "w") as f:
        f.write(os.environ["GOOGLE_JSON"])

app = Flask(__name__, static_folder='public', static_url_path='')
sock = Sock(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bulut-anahtar.json"
proje_id = "project-805b15f1-d114-4cb0-862"
konu_id = "hediye-akisi"

yayinlayici = pubsub_v1.PublisherClient()
konu_yolu = yayinlayici.topic_path(proje_id, konu_id)

client = MongoClient("mongodb+srv://senatavv:sena6432@cluster0.5urrqbx.mongodb.net/?appName=Cluster0")
db = client["HediyeRehberiDB"]
koleksiyon = db["AnlikVeriler"]

istatistikler = {
    "Teknoloji": 0,
    "Aksesuar": 0,
    "Deneyim": 0,
    "Gurme": 0,
    "Sanat": 0,
    "Spor": 0,
    "Ev-Dekor": 0
}

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@sock.route('/ws')
def handle_websocket(ws):
    print("\n--- Gerçek Zamanlı Veri Akışı Başladı ---")
    while True:
        data = ws.receive()
        veri = json.loads(data)
        veri["zaman_damgasi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    
        try:
            mesaj_verisi = json.dumps(veri).encode("utf-8")
            future = yayinlayici.publish(konu_yolu, mesaj_verisi)
            print(f"[GOOGLE CLOUD] Veri Pub/Sub'a gönderildi. ID: {future.result()}")
        except Exception as e:
            print(f"[GOOGLE CLOUD HATASI] {e}")

        try:
            koleksiyon.insert_one(veri.copy())
            print(f"[MONGODB ATLAS] Veri buluta kaydedildi!")
        except Exception as e:
            print(f"[MONGODB HATASI] {e}")

        guncel_kategori = None

        if veri.get('tip') == "KULLANICI_PROFILI":
            ilgi = veri.get('ilgi_alani')
            guncel_kategori = ilgi
            if ilgi in istatistikler:
                istatistikler[ilgi] += 1
                
        elif veri.get('tip') == "HEDIYE_TIKLAMA":
            kat = veri.get('kat')
            guncel_kategori = kat
            if kat in istatistikler:
                istatistikler[kat] += 1

        en_cok_ilgi = max(istatistikler, key=istatistikler.get)
        
        print(f">>> ANLIK İŞLEM : Veri analize dahil edildi.")
        print(f">>> GENEL ANALİZ: Şu an lider kategori: {en_cok_ilgi} ({istatistikler[en_cok_ilgi]} puan)")
        print("-" * 50)

if __name__ == '__main__':
    app.run(port=3000)
