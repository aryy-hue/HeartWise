import os

# Mengambil konfigurasi dari Environment Variables yang kita set di Docker.
# Jika variabel tidak ditemukan, ia akan menggunakan nilai default (argumen kedua).
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "cardio_app")
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
GCS_KEYFILE_PATH = (
    "C:/Users/wardh/Downloads/credentials/uascloud-462303-9af78e58fe6e.json"
)

GCS_BUCKET_NAME = "medicalhealth-106-135"
