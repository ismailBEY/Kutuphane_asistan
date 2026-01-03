from flask import Blueprint, jsonify, request
import requests
import json

books_bp = Blueprint('books', __name__)

# OLLAMA AYARLARI
# Docker içinden ana makineye (localhost) ulaşmak için bu özel adresi kullanıyoruz:
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
OLLAMA_MODEL = "gemma:2b"  # İndirdiğin modelin adı

@books_bp.route('/search', methods=['GET'])
def search_book():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Lutfen bir kitap adi girin"}), 400

    # 1. Open Library Araması (Aynı kalıyor)
    url = f"https://openlibrary.org/search.json?q={title}&limit=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("numFound", 0) == 0:
            return jsonify({"message": "Kitap bulunamadi"}), 404
            
        book = data["docs"][0]
        real_title = book.get("title")
        author = book.get("author_name", ["Bilinmiyor"])[0]
        year = book.get("first_publish_year", 0)

        # 2. OLLAMA (Yerel Yapay Zeka) Analizi
        ai_context = "Analiz hazirlaniyor..."
        
        prompt = (
            f"'{real_title}' kitabını yazan {author} hakkında Türkçe bilgi ver. "
            f"Kitabın yazıldığı dönem, yazarın ruh hali ve kitabın önemi nedir? "
            f"Çok kısa, tek bir paragraf ve samimi bir dille özetle."
        )

        # Ollama'ya istek atılacak veri paketi
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False  # Cevabı parça parça değil, tek seferde istiyoruz
        }

        print(f"🦙 Ollama'ya soruluyor: {real_title}...")

        try:
            # Docker içinden dışarıdaki Ollama'ya istek atıyoruz
            ollama_response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            
            if ollama_response.status_code == 200:
                # Ollama'dan gelen JSON cevabını çözümlüyoruz
                ai_result = ollama_response.json()
                ai_context = ai_result.get("response", "Cevap boş döndü.")
            else:
                ai_context = f"Ollama Hatası: {ollama_response.status_code}"
                print(f"Ollama Hata Detayı: {ollama_response.text}")

        except requests.exceptions.ConnectionError:
            ai_context = "⚠️ Hata: Ollama uygulamasına ulaşılamadı. Çalışıyor mu?"
        except Exception as e:
            ai_context = f"⚠️ Beklenmedik Hata: {str(e)}"

        return jsonify({
            "title": real_title,
            "author": author,
            "year": year,
            "source": "Open Library + Local Ollama (Gemma)",
            "context": ai_context
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
