# 1. Python bazlı hafif bir imaj kullan
FROM python:3.10-slim

# 2. Çalışma dizini oluştur
WORKDIR /app

# 3. Gereken dosyaları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# 4. Geri kalan tüm dosyaları kopyala
COPY . .

# 5. Ortam değişkenlerini tanımla
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 6. Portu dışa aç
EXPOSE 5000

# 7. Uygulamayı başlat
CMD ["flask", "run"]


COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh