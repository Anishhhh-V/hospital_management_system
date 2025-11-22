USE hospital_db;

INSERT INTO Users (username, password_hash, full_name, role) VALUES
('admin', '$2b$12$placeholderhash_admin', 'Administrator', 'Admin'),
('dr1', '$2b$12$placeholderhash_doc', 'Dr One', 'Doctor'),
('nurse1', '$2b$12$placeholderhash_nurse', 'Nurse One', 'Nurse');
