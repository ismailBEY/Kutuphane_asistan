from mcp.server.fastmcp import FastMCP
import requests

# 1. Servisi Oluşturuyoruz
# "KutuphaneAjanı" adında bir MCP sunucusu tanımladık.
mcp = FastMCP("Kutuphane Ajanı")

# ---------------------------------------------------------
# TOOL 1: Basit İşlem (Ödev Şartı: Herhangi bir işlem)
# ---------------------------------------------------------
@mcp.tool()
def toplama_yap(sayi1: int, sayi2: int) -> int:
    """
    İki sayıyı toplar. Basit matematiksel işlem örneğidir.
    """
    return sayi1 + sayi2

# ---------------------------------------------------------
# TOOL 2: Public API Sorgusu (Ödev Şartı: Request kullanımı)
# ---------------------------------------------------------
@mcp.tool()
def kitap_bilgisi_getir(kitap_adi: str) -> str:
    """
    Google Books Public API servisine istek atarak kitap hakkında
    başlık, yazar ve yıl bilgisini getirir.
    Args:
        kitap_adi: Aranacak kitabın ismi (Örn: Nutuk, Sefiller)
    """
    # Public API Adresi
    url = "https://www.googleapis.com/books/v1/volumes"
    
    # Parametreler
    params = {
        "q": f"intitle:{kitap_adi}",
        "maxResults": 1
    }

    try:
        # REQUEST Kütüphanesi ile Dış Dünyaya İstek (Ödevin kritik noktası)
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return "Hata: API servisine ulaşılamadı."

        data = response.json()
        
        # Gelen veriyi kontrol et
        if "items" not in data:
            return "Üzgünüm, bu isimde bir kitap bulunamadı."

        # Veriyi ayıkla (Parsing)
        kitap = data["items"][0]["volumeInfo"]
        baslik = kitap.get("title", "Bilinmiyor")
        yazar = kitap.get("authors", ["Yazar Bilinmiyor"])[0]
        tarih = kitap.get("publishedDate", "Tarih Yok")[:4] # Sadece yılı al

        # Sonucu metin olarak döndür
        return f"📖 Kitap: {baslik} | ✍️ Yazar: {yazar} | 📅 Yıl: {tarih}"

    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

# Servisi başlat (Eğer bu dosya doğrudan çalıştırılırsa)
if __name__ == "__main__":
    mcp.run()
