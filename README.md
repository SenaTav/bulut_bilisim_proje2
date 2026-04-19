#  Bulut Tabanlı Gerçek Zamanlı Veri Akışı 

Bu proje, "Bulut Bilişim" dersi için geliştirilmiş, IoT simülasyonundan alınan gerçek zamanlı verilerin işlendiği, bulut mesajlaşma kuyruğuna (Google Cloud Pub/Sub) aktarıldığı ve bulut veritabanında (MongoDB Atlas) depolanıp anlık olarak analiz edildiği tam teşekküllü bir sistem mimarisidir.

**Canlı Demo:** [Projeyi İncele](https://hediye-rehberi-projesi.onrender.com/) 

---

##  Sistem Mimarisi ve Veri Yolculuğu

Sistem 4 ana katmandan oluşmaktadır:

1. **İstemci (Web Arayüzü / IoT Simülasyonu):** Kullanıcı etkileşimleri anlık veri paketi (JSON) olarak üretilir.
2. **Sunucu (Python Flask & WebSocket):** İstemciden gelen veriler `wss://` (WebSocket) protokolü ile kesintisiz ve gerçek zamanlı olarak sunucuya alınır. Zaman damgası eklenerek zenginleştirilir.
3. **Bulut Veri Akışı (Google Cloud Pub/Sub):** Sunucudaki veriler, yüksek trafik durumlarında kaybolmaması ve sıraya sokulması için asenkron olarak GCP Pub/Sub Topic'ine fırlatılır.
4. **Bulut Veritabanı ve Analiz (MongoDB Atlas):** Veriler güvenli bir şekilde NoSQL bulut veritabanına kaydedilir. Eş zamanlı olarak sunucu tarafında işlenerek "Anlık Analiz Merkezi" üzerinden lider kategoriler hesaplanır.

---

##  Kullanılan Teknolojiler

* **Backend:** Python 3, Flask, Flask-Sock (WebSocket)
* **Cloud Messaging Pipeline:** Google Cloud Pub/Sub
* **Cloud Database:** MongoDB Atlas (PyMongo)
* **Deployment:** Render 
* **Frontend:** HTML, CSS3, JavaScript (WebSocket API)

---

##  Kurulum ve Lokal Çalıştırma (Geliştiriciler İçin)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### Ön Koşullar
* Python 3.x yüklü olmalıdır.
* Google Cloud hesabınızda Pub/Sub aktif edilmeli ve bir Service Account `.json` anahtarı alınmalıdır.
* MongoDB Atlas üzerinde bir cluster oluşturulmalıdır.

### Adımlar

1. **Repoyu Klonlayın:**
   ```bash
  git clone https://github.com/SenaTav/bulut_bilisim_proje2.git
