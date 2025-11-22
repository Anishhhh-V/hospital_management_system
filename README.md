This is a simple web app to manage patients, beds, doctors, and admissions.

Features
- Add new patients
- Admit patients to available beds
- Discharge patients
- Beds update automatically (occupied/free)
- Alerts when beds are almost full
- Login system (Admin, Doctor, Nurse)

How to Run
1. Install Python + MySQL
2. Run SQL files in the `sql` folder (01, 02, 03)
3. Open backend folder and install packages:
   - python -m venv venv
   - venv\Scripts\activate
   - pip install -r requirements.txt
4. Create users:
   - python create_user.py
5. Start the app:
   - python app.py
6. Open browser:
   - http://127.0.0.1:5000

Default Logins
Admin → admin / Admin@123  
Doctor → dr1 / Doctor@123  
Nurse → nurse1 / Nurse@123
