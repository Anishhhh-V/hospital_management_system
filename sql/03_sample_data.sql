USE hospital_db;

INSERT INTO Patients (name, age, disease) VALUES
('Rohan', 34, 'Dengue'),
('Aarav', 20, 'Pneumonia'),
('Sita', 45, 'Fracture'),
('Meena', 60, 'Covid');

INSERT INTO Doctors (name, speciality) VALUES
('Dr. Sharma', 'General Medicine'),
('Dr. Gupta', 'Orthopedic'),
('Dr. Khan', 'Pulmonology');

INSERT INTO Beds (ward) VALUES
('A1'),('A1'),('B1'),('B1'),('ICU'),('ICU');
