from mcp.server.fastmcp import FastMCP
import requests

# Servis Adı
mcp = FastMCP("Yerel Kütüphane Baglantisi")

@mcp.tool()
def yerel_kutuphaneden_sorgula(kitap_adi: str) -> str:
    """
    Bizim kendi Flask Backend'imize istek atarak kitap bilgisi getirir.
    """
    # Docker/Localhost adresimiz
    api_url = "http://localhost:5000/api/search"
    
    try:
        # Flask API'mize istek atıyoruz
        response = requests.get(api_url, params={"title": kitap_adi})
        
        if response.status_code == 200:
            data = response.json()
            return f"📘 BULUNDU: '{data['title']}' - Yazar: {data['author']} ({data['year']})"
        elif response.status_code == 404:
            return "Kitap bulunamadı."
        else:
            return f"Hata oluştu: {response.status_code}"
            
    except Exception as e:
        return f"Backend servisine ulaşılamadı: {str(e)}"

if __name__ == "__main__":
    # TEST ETMEK ICIN:
    # Asagidaki 'print' satirinin basindaki # isaretini kaldir ve kaydet.
    # Terminalde "python mcp_server.py" yazinca sonucu goreceksin.
    
    print("--- Test Basliyor ---")
    sonuc = yerel_kutuphaneden_sorgula("satranc")
    print(sonuc)
    print("--- Test Bitti ---")

    # GERCEK SUNUCU MODU (Hocaya teslim ederken burasi acik olsun):
    # mcp.run()