from mcp.server.fastmcp import FastMCP
import requests
import sys

# Servisimizin Adı
mcp = FastMCP("Süper Kütüphane Asistanı")

# ----------------------------------------------------------------
# YETENEK 1: Open Library (Ödev Şartı: Public & Uzak API)
# ----------------------------------------------------------------
@mcp.tool()
def open_library_hizli_arama(kitap_adi: str) -> str:
    """
    ÖDEV İÇİN: Open Library (Public API) üzerinden yazar ve yıl bilgisi çeker.
    Bu fonksiyon direkt dış dünyaya bağlanır.
    """
    url = "https://openlibrary.org/search.json"
    print(f"🌍 [Public API] Open Library'e gidiliyor: {kitap_adi}...")
    
    try:
        response = requests.get(url, params={"q": kitap_adi, "limit": 1}, timeout=10)
        data = response.json()
        
        if data.get("numFound", 0) == 0:
            return "❌ Kitap bulunamadı."
            
        kitap = data["docs"][0]
        baslik = kitap.get("title")
        yazar = kitap.get("author_name", ["Bilinmiyor"])[0]
        yil = kitap.get("first_publish_year", "Bilinmiyor")
        
        return f"📖 {baslik} | ✍️ {yazar} | 📅 {yil} (Kaynak: Open Library)"
        
    except Exception as e:
        return f"Public API Hatası: {str(e)}"

# ----------------------------------------------------------------
# YETENEK 2: Detaylı Analiz (Proje Özelliği: Localhost & AI)
# ----------------------------------------------------------------
@mcp.tool()
def yerel_yapay_zeka_analizi(kitap_adi: str) -> str:
    """
    PROJE İÇİN: Docker'daki Flask + Ollama sistemine bağlanır.
    Kitabın özetini ve yapay zeka yorumunu getirir.
    """
    url = "http://localhost:5000/api/search"
    print(f"🏠 [Local API] Kendi sunucumuza gidiliyor: {kitap_adi}...")
    
    try:
        # Kendi backend'imize istek atıyoruz
        response = requests.get(url, params={"title": kitap_adi})
        
        if response.status_code == 200:
            data = response.json()
            # Backend'den gelen 'context' (AI yorumu) bilgisini alıyoruz
            ai_yorumu = data.get("context", "Yorum yok.")
            kaynak = data.get("source", "Bilinmiyor")
            
            return (
                f"🧠 YAPAY ZEKA ANALİZİ:\n"
                f"--------------------------------------\n"
                f"{ai_yorumu}\n"
                f"--------------------------------------\n"
                f"(Kaynak: {kaynak})"
            )
        else:
            return "❌ Yerel sunucuda kitap bulunamadı."
            
    except requests.exceptions.ConnectionError:
        return "⚠️ HATA: Docker/Flask sunucun çalışmıyor! Önce 'docker-compose up' yapmalısın."
    except Exception as e:
        return f"Beklenmedik hata: {str(e)}"

# ----------------------------------------------------------------
# TEST MENU (Dosyayı çalıştırınca seçim yapabilirsin)
# ----------------------------------------------------------------
if __name__ == "__main__":
    print("\n--- MCP SERVER TEST PANELİ ---")
    print("1. Open Library (Public API - Sadece Yıl/Yazar)")
    print("2. Yerel Analiz (Localhost - Yapay Zeka Yorumu)")
    
    secim = input("Seçiminiz (1 veya 2): ")
    kitap = input("Aranacak Kitap Adı (Örn: Nutuk): ") or "Nutuk"
    
    print("\n--- Sonuç Hesaplanıyor ---\n")
    
    if secim == "1":
        print(open_library_hizli_arama(kitap))
    elif secim == "2":
        print(yerel_yapay_zeka_analizi(kitap))
    else:
        print("Geçersiz seçim.")
