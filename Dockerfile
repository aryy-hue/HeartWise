# 1. Pilih base image Python
FROM python:3.9-slim

# 2. Install dependensi sistem yang dibutuhkan oleh WeasyPrint
# Menambahkan libpangoft2-1.0-0 yang sebelumnya kurang
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 3. Atur direktori kerja di dalam container
WORKDIR /app

# 4. Salin file requirements.txt dan install semua library Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin seluruh kode proyek Anda
COPY . .

# 6. Expose port yang akan digunakan
EXPOSE 5000

# 7. Definisikan perintah untuk menjalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]