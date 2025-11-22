DROP DATABASE IF EXISTS hospital_db;
CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    disease VARCHAR(100)
);

CREATE TABLE Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    speciality VARCHAR(100)
);

CREATE TABLE Beds (
    bed_id INT AUTO_INCREMENT PRIMARY KEY,
    ward VARCHAR(50),
    is_occupied BOOLEAN DEFAULT FALSE
);

CREATE TABLE Admissions (
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    bed_id INT,
    doctor_id INT,
    admit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    discharge_time DATETIME NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (bed_id) REFERENCES Beds(bed_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    role ENUM('Admin','Doctor','Nurse') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(100),
    message VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT FALSE
);

CREATE TABLE Thresholds (
    id INT PRIMARY KEY,
    min_free_beds INT DEFAULT 1
);

INSERT INTO Thresholds (id, min_free_beds) VALUES (1,1)
ON DUPLICATE KEY UPDATE min_free_beds = min_free_beds;
