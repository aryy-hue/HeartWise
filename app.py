from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from joblib import load
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY
from weasyprint import HTML
from google.cloud import storage
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = SECRET_KEY

try:
    storage_client = storage.Client()
    # GANTI DENGAN NAMA BUCKET ANDA
    GCS_BUCKET_NAME = "medicalhealth-106-135"
except Exception as e:
    print(f"Peringatan: Gagal menginisialisasi Google Cloud Storage client: {e}")
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

    # 1. Ambil dan susun data dari form
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

    # 2. Lakukan prediksi dengan model
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

    # 3. Simpan ke database dan dapatkan ID nya
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
        diagnosis_id = cursor.lastrowid  # Ambil ID baris yang baru saja dimasukkan
    except Exception as e:
        print(f"Error saat menyimpan ke DB: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # Siapkan data untuk ditampilkan dan dikirim ke template PDF
    result = {
        "patient_data": data,
        "cluster": int(cluster),
        "risk_level": risk_level,
        "recommendation": recommendation,
    }

    # 4. Proses pembuatan PDF dan upload ke GCS (di latar belakang)
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

            flash(
                f"Laporan diagnosis (ID: {diagnosis_id}) berhasil diarsipkan.",
                "success",
            )

        except Exception as e:
            print(f"Error saat membuat/mengunggah PDF untuk ID {diagnosis_id}: {e}")
            flash(f"Gagal mengarsipkan laporan PDF (ID: {diagnosis_id}).", "danger")

    # 5. Tampilkan halaman result.html ke pengguna (ini harus jadi baris terakhir)
    return render_template("result.html", result=result)


# Admin routes


@app.route("/admin")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("index"))
    return render_template("admin_dashboard.html")


@app.route("/admin/users")
def admin_users():
    if not session.get("is_admin"):
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, is_admin FROM user")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin_users.html", users=users)


@app.route("/admin/diagnosis")
def admin_diagnosis():
    if not session.get("is_admin"):
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT diagnosis.*, user.username 
        FROM diagnosis 
        JOIN user ON diagnosis.user_id = user.id 
        ORDER BY diagnosis.created_at DESC
    """
    )
    diagnoses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin_diagnosis.html", diagnoses=diagnoses)


if __name__ == "__main__":
    app.run(debug=True)
