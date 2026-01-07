FROM python:3.10-slim

WORKDIR /app

# SİSTEM GÜNCELLEMESİ (Kritik Adım)
# google-generativeai ve grpcio için gerekli derleme araçlarını yüklüyoruz
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Pip'i güncelle ve kütüphaneleri yükle
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
