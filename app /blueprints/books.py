from flask import Blueprint, jsonify, request
import requests

# Blueprint Tanımlaması
books_bp = Blueprint('books', __name__)

@books_bp.route('/search', methods=['GET'])
def search_book():
    """
    Kitap arama servisi.
    ---
    tags:
      - Kitaplar
    parameters:
      - name: title
        in: query
        type: string
        required: true
        default: Nutuk
        description: Aranacak kitabin adi
    responses:
      200:
        description: Kitap bilgisi basariyla dondu
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            year:
              type: integer
      404:
        description: Kitap bulunamadi
    """
    # Parametreyi al
    title = request.args.get('title')
    
    # Eger parametre yoksa hata don
    if not title:
        return jsonify({"error": "Lutfen bir kitap adi girin (Orn: ?title=Nutuk)"}), 400

    # Open Library API'ye istek at
    url = f"https://openlibrary.org/search.json?q={title}&limit=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Sonuc kontrolu
        if data.get("numFound", 0) == 0:
            return jsonify({"message": "Kitap bulunamadi"}), 404
            
        book = data["docs"][0]
        
        # Veriyi hazırla ve dondur
        return jsonify({
            "title": book.get("title"),
            "author": book.get("author_name", ["Bilinmiyor"])[0],
            "year": book.get("first_publish_year", 0),
            "source": "Open Library API"
        })
        
    except Exception as e:
        return jsonify({"error": f"Bir hata olustu: {str(e)}"}), 500
