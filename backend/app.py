import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import get_conn
from auth import User

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey")

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id, username, full_name, role FROM Users WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if row:
        return User(row['user_id'], row['username'], row['full_name'], row['role'])
    return None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Users WHERE username=%s", (uname,))
        row = cur.fetchone()
        cur.close(); conn.close()

        if row and bcrypt.check_password_hash(row['password_hash'], pwd):
            user = User(row['user_id'], row['username'], row['full_name'], row['role'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # stats
    cur.execute("SELECT COUNT(*) AS total_beds, SUM(is_occupied) AS occupied FROM Beds")
    stats = cur.fetchone()

    # all beds
    cur.execute("SELECT * FROM Beds")
    beds = cur.fetchall()

    # current admissions
    cur.execute("""
        SELECT a.admission_id, p.name AS patient, b.ward, 
               d.name AS doctor, a.admit_time
        FROM Admissions a
        JOIN Patients p ON p.patient_id = a.patient_id
        JOIN Doctors d ON d.doctor_id = a.doctor_id
        JOIN Beds b ON b.bed_id = a.bed_id
        WHERE a.discharge_time IS NULL
    """)
    admissions = cur.fetchall()

    # load patients (for dropdown)
    cur.execute("SELECT * FROM Patients")
    patients = cur.fetchall()

    # load doctors
    cur.execute("SELECT * FROM Doctors")
    doctors = cur.fetchall()

    # load free beds
    cur.execute("SELECT * FROM Beds WHERE is_occupied = FALSE")
    free_beds = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'dashboard.html',
        stats=stats,
        beds=beds,
        admissions=admissions,
        patients=patients,
        doctors=doctors,
        free_beds=free_beds
    )

@app.route('/admit', methods=['POST'])
@login_required
def admit():
    patient_id = request.form['patient_id']
    bed_id = request.form['bed_id']
    doctor_id = request.form['doctor_id']

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Admissions (patient_id, bed_id, doctor_id)
        VALUES (%s, %s, %s)
    """, (patient_id, bed_id, doctor_id))
    conn.commit()
    cur.close(); conn.close()

    flash("Patient admitted successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/discharge/<int:admission_id>', methods=['POST'])
@login_required
def discharge(admission_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Admissions 
        SET discharge_time = NOW()
        WHERE admission_id = %s
    """, (admission_id,))
    conn.commit()
    cur.close(); conn.close()

    flash("Patient discharged!", "success")
    return redirect(url_for('dashboard'))

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Patients (name, age, disease)
        VALUES (%s, %s, %s)
    """, (name, age, disease))
    conn.commit()
    cur.close(); conn.close()

    flash("New patient added!", "success")
    return redirect(url_for('dashboard'))

@app.route('/api/alerts')
@login_required
def api_alerts():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Alerts WHERE is_resolved = FALSE ORDER BY created_at DESC")
    alerts = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(alerts)

@app.route('/alert/resolve/<int:alert_id>', methods=['POST'])
@login_required
def resolve_alert(alert_id):

    if current_user.role != "Admin":
        flash("Only Admin can resolve alerts!", "danger")
        return redirect(url_for("dashboard"))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE Alerts SET is_resolved = TRUE WHERE alert_id = %s", (alert_id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Alert resolved!", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
