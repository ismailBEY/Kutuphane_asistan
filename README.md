# Library Assistant API

Bu proje, kitap arama ve yapay zeka destekli kitap inceleme servisi sunar. Kullanıcılar ayrıca kayıt olup favori kitaplarını saklayabilirler.

## Proje Hakkında
Bu proje Docker konteynerleri üzerinde çalışacak şekilde tasarlanmıştır. `Flasgger` ile otomatik API dokümantasyonu sunar ve JWT tabanlı kimlik doğrulama kullanır.

## Başlangıç (Kurulum)

1. Docker ve Docker Compose'un yüklü olduğundan emin olun.
2. Proje dizininde terminali açın.
3. Aşağıdaki komutla projeyi başlatın:
   ```bash
   docker-compose down -v  # (Opsiyonel) Temizlik için
   docker-compose up --build -d
   ```
4. Uygulama ve Arayüz: `http://localhost:5000`
5. Swagger Dokümanı: `http://localhost:5000/apidocs`

## Özellikler
- **Kitap Arama:** OpenLibrary API ve Yerel Ollama AI (Gemma) entegrasyonu.
- **Kullanıcı İşlemleri:** Kayıt olma ve Giriş yapma (JWT).
- **Favoriler:** Giriş yapmış kullanıcılar kitapları favorilerine ekleyebilir.
- **Arayüz (Frontend):** Giriş, Kayıt, Arama ve Favori Listeleme tek bir sayfada çalışır.

## Veritabanı
Proje **PostgreSQL** kullanmaktadır. Docker compose içinde otomatik olarak ayağa kalkar.

## Test
Otomatik testleri çalıştırmak için:
```bash
python test_api.py
```

## Sistem Akışı (Sequence Diagram)

Aşağıdaki diyagram, bir kullanıcının kitabı arayıp favorilerine ekleme sürecini göstermektedir.

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Frontend as Arayüz (Web)
    participant API as Python API (Flask)
    participant DB as Veritabanı (PostgreSQL)
    participant External as OpenLibrary API
    participant AI as Ollama (AI Model)

    User->>Frontend: Kitap İsmi Girer (örn: Nutuk)
    Frontend->>API: GET /api/search?title=Nutuk
    API->>External: Kitap Bilgisi İste
    External-->>API: Yazar, Yıl, Başlık Dön
    API->>AI: "Bu kitap hakkında özet yaz"
    AI-->>API: AI Özeti (Context)
    API-->>Frontend: JSON Yanıt (Kitap + AI Özeti)
    Frontend-->>User: Kitap Detaylarını Gösterir

    Note over User, DB: Favorilere Ekleme (Auth Gerektirir)

    User->>Frontend: "Favorilere Ekle" Butonuna Basar
    Frontend->>API: POST /api/favorite (Token ile)
    
    alt Token Geçersiz/Yok
        API-->>Frontend: 401 Unauthorized
        Frontend-->>User: "Lütfen Giriş Yapın" der
    else Token Geçerli
        API->>DB: Kitabı Favorilere Kaydet
        DB-->>API: Onay (Success)
        API-->>Frontend: 201 Created
        Frontend-->>User: "Favorilere Eklendi!"
    end
```
