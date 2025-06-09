# 1. Python bazlı hafif bir imaj kullan
FROM python:3.10-slim

# 2. Çalışma dizini oluştur
WORKDIR /app

# 3. Gereken dosyaları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Geri kalan tüm dosyaları kopyala (wait-for-it.sh içinde yer almalıysa burada olur)
COPY . .

# 5. Ortam değişkenlerini tanımla
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 6. wait-for-it.sh'e çalıştırma izni ver
RUN chmod +x /app/wait-for-it.sh

# 7. Portu dışa aç
EXPOSE 5000

# 8. Uygulamayı başlat
CMD ["./wait-for-it.sh", "db:5432", "--", "flask", "run"]
