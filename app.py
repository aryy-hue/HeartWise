from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    Response,
)
import pandas as pd
from joblib import load
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY
from config import GCS_KEYFILE_PATH, GCS_BUCKET_NAME
from weasyprint import HTML, CSS
from google.cloud import storage
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

try:
    # Cek: Apakah pemilik memberikan lokasi kunci rahasia?
    if GCS_KEYFILE_PATH:
        # Jika YA, gunakan kunci dari lokasi tersebut.
        storage_client = storage.Client.from_service_account_json(GCS_KEYFILE_PATH)
        print("Info: Terhubung ke GCS menggunakan file kunci.")
    else:
        # Jika TIDAK, coba saja masuk (mungkin ada cara lain seperti 'gcloud login')
        storage_client = storage.Client()
        print("Peringatan: Tidak ada file kunci, mencoba koneksi default.")

except Exception as e:
    print(f"KRITIS: Gagal total terhubung ke Google Cloud Storage: {e}")
    storage_client = None

# Load model
model_data = load("cardio_clustering_model.joblib")
kmeans = model_data["kmeans"]
scaler = model_data["scaler"]

# Risk labels and recommendations
risk_labels = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}

recommendations = {
    0: "Tidak memerlukan rujukan spesialis jantung. Rutin pemeriksaan kesehatan umum.",
    1: "Direkomendasikan rujukan ke spesialis jantung untuk evaluasi lebih lanjut.",
    2: "RUJUK SEGERA ke spesialis jantung. Kondisi berisiko tinggi!",
}


# DB Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    return conn


# Routes


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )
            conn.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("Username already exists.", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]
            flash("Login successful.", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("login"))


@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # 1. Ambil data dari form (kode ini sudah benar)
    data = {
        "Age": float(request.form["age"]),
        "Gender": 1 if request.form["gender"] == "male" else 0,
        "Heart rate": float(request.form["heart_rate"]),
        "Systolic blood pressure": float(request.form["systolic"]),
        "Diastolic blood pressure": float(request.form["diastolic"]),
        "Blood sugar": float(request.form["blood_sugar"]),
        "CK-MB": float(request.form["ck_mb"]),
        "Troponin": float(request.form["troponin"]),
        "Result": request.form["result"],
    }

    # 2. Lakukan prediksi (kode ini sudah benar)
    df = pd.DataFrame([data])
    features = [
        "Age",
        "Gender",
        "Heart rate",
        "Systolic blood pressure",
        "Diastolic blood pressure",
        "Blood sugar",
        "CK-MB",
        "Troponin",
    ]
    X = df[features]
    X_scaled = scaler.transform(X)
    cluster = kmeans.predict(X_scaled)[0]
    risk_level = risk_labels.get(cluster, "Unknown")
    recommendation = recommendations.get(cluster, "Konsultasi dokter umum diperlukan.")

    # 3. Simpan ke database (kode ini sudah benar)
    diagnosis_id = None
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO diagnosis 
            (user_id, age, gender, heart_rate, systolic_bp, diastolic_bp, blood_sugar, ck_mb, troponin, result, cluster, risk_level, recommendation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                data["Age"],
                data["Gender"],
                data["Heart rate"],
                data["Systolic blood pressure"],
                data["Diastolic blood pressure"],
                data["Blood sugar"],
                data["CK-MB"],
                data["Troponin"],
                data["Result"],
                int(cluster),
                risk_level,
                recommendation,
            ),
        )
        conn.commit()
        diagnosis_id = cursor.lastrowid
    except Exception as e:
        print(f"Error saat menyimpan ke DB: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # Siapkan data untuk ditampilkan
    result = {
        "patient_data": data,
        "cluster": int(cluster),
        "risk_level": risk_level,
        "recommendation": recommendation,
    }

    # --- PERUBAHAN UTAMA ADA DI SINI ---
    gcs_upload_success = False
    pdf_public_url = None

    # 4. Proses pembuatan PDF dan upload ke GCS
    if diagnosis_id and storage_client:
        try:
            wib = pytz.timezone("Asia/Jakarta")
            generation_time = datetime.now(wib).strftime("%d %B %Y, %H:%M:%S WIB")

            html_string = render_template(
                "result_pdf.html",
                result=result,
                diagnosis_id=diagnosis_id,
                generation_time=generation_time,
            )
            pdf_bytes = HTML(string=html_string).write_pdf()
            destination_blob_name = (
                f"laporan-diagnosis/diagnosis-report-{diagnosis_id}.pdf"
            )

            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(pdf_bytes, content_type="application/pdf")

            # Jadikan file bisa diakses publik dan dapatkan URL-nya
            blob.make_public()
            pdf_public_url = blob.public_url
            gcs_upload_success = True

        except Exception as e:
            print(f"Error saat membuat/mengunggah PDF untuk ID {diagnosis_id}: {e}")
            gcs_upload_success = False

    # 5. Tampilkan halaman result.html dengan data tambahan untuk tombol dan pop-up
    return render_template(
        "result.html",
        result=result,
        diagnosis_id=diagnosis_id,
        gcs_upload_success=gcs_upload_success,
        pdf_url=pdf_public_url,
    )


@app.route("/download_pdf/<int:diagnosis_id>")
def download_pdf(diagnosis_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # 1. Ambil data diagnosis dari database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM diagnosis WHERE id = %s", (diagnosis_id,))
    diagnosis = cursor.fetchone()
    conn.close()

    if not diagnosis:
        return "Diagnosis tidak ditemukan!", 404

    # 2. Susun kembali data seperti format 'result'
    result = {
        "patient_data": {
            "Age": diagnosis["age"],
            "Gender": diagnosis["gender"],
            "Heart rate": diagnosis["heart_rate"],
            "Systolic blood pressure": diagnosis["systolic_bp"],
            "Diastolic blood pressure": diagnosis["diastolic_bp"],
            "Blood sugar": diagnosis["blood_sugar"],
            "CK-MB": diagnosis["ck_mb"],
            "Troponin": diagnosis["troponin"],
            "Result": diagnosis["result"],
        },
        "risk_level": diagnosis["risk_level"],
        "recommendation": diagnosis["recommendation"],
    }

    # 3. Render template PDF dan generate PDF
    wib = pytz.timezone("Asia/Jakarta")
    generation_time = datetime.now(wib).strftime("%d %B %Y, %H:%M:%S WIB")
    html_string = render_template(
        "result_pdf.html",
        result=result,
        diagnosis_id=diagnosis_id,
        generation_time=generation_time,
    )
    pdf_bytes = HTML(string=html_string).write_pdf()

    # 4. Kirim file ke browser sebagai download
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-disposition": f"attachment; filename=diagnosis-report-{diagnosis_id}.pdf"
        },
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True)
