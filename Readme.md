# 🔍 LocateU — Lost & Found Management System

LocateU is a **Flask + MySQL web application** designed to simplify the process of reporting, tracking, and claiming lost or found items within an institution. It features student and staff dashboards, image uploads, notifications, and automated item matching.

---

## ⚙️ Features

- 👤 **Student Portal** – Register, log in, and report lost or found items  
- 📝 **Staff Portal** – Review reports, verify ownership, and confirm claims  
- 🖼️ **Image Uploads** – Attach item photos for easier identification  
- 🔔 **Notifications** – Real-time updates for claims and matches  
- 🤖 **Smart Matching** – Automatically suggests potential lost–found matches  
- 💎 **SQL Scripts & ER Diagram** – Database schema and stored functions included  

---

## 🧠 System Overview

### 🧩 Backend (Flask)
- Developed using **Flask** with `mysql-connector` for database communication.  
- Modular architecture with routes for student and staff operations.  
- Implements authentication, session handling, and notification APIs.  

### 🎨 Frontend
- Built using **Jinja2**, **HTML**, **CSS**, and **JavaScript**.  
- Clean and responsive design for login, registration, and dashboards.  

### 🗄️ Database
- **MySQL** database with tables for users, items, and claims.  
- Includes SQL setup scripts and an ER diagram in the `/Docs` folder.  

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Pratheek22/LocateU-Lost-And-Found-System.git
cd LocateU-Lost-And-Found-System-main
```

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
pip install flask python-dotenv mysql-connector-python
```

### 3. Configure Environment
Create a **.env** file in the project root with:
```
# Database Configuration
DB_HOST=localhost
DB_NAME=lostandfounddb
DB_USER=root
DB_PASSWORD=******  
DB_CHARSET=utf8mb4

# Application Settings
APP_DEBUG=True
APP_SECRET_KEY=secret_key
```

### 4. Setup Database
- Run the SQL scripts in `/Docs` to create database schema and procedures.  
- Verify tables and relationships via the included **ER Diagram**.  

### 5. Run the Application
```bash
cd Backend
python app.py
```
Visit **http://127.0.0.1:5000/** in your browser 🎉

---

## 🔋 Project Structure
```
Backend/
 ├─ app.py              # Main Flask application
 ├─ config.py           # Configuration handler
 └─ database.py         # Database functions
frontend/
 ├─ templates/          # HTML templates
 └─ static/             # CSS & JS files
Docs/
 ├─ schema.sql
 ├─ functions.sql
 └─ ER_Diagram.png
```

---

## 🔮 Future Enhancements
- 🧠 AI-based image similarity matching  
- 🖼️ Cloud-based image storage (AWS S3 / Firebase)  
- 📱 Fully responsive mobile interface  
- 🔐 Advanced authentication and role management  

---

## 👨‍💻 Authors
**Developed by:** Pratheek J Gowda  , Rajat Ramakrishna Bhat
**Institution:** PES University  
**Course:** UE23CS351A - DBMS Mini Project  


<img width="1920" height="1547" alt="screencapture-127-0-0-1-5000-student-dashboard-2025-11-08-18_41_29" src="https://github.com/user-attachments/assets/bcc8a3d6-d7f8-45d4-8ec8-e30eb6f3b9c4" />

<img width="1002" height="536" alt="image" src="https://github.com/user-attachments/assets/9b4bbe64-daf4-4cad-93ab-ad539651febf" />

<img width="1920" height="1549" alt="screencapture-127-0-0-1-5000-staff-dashboard-2025-11-08-18_44_03" src="https://github.com/user-attachments/assets/aeb9048e-1721-4c86-ad88-e476c8b78612" />

<img width="1920" height="4170" alt="screencapture-127-0-0-1-5000-staff-claims-2025-11-08-18_44_22" src="https://github.com/user-attachments/assets/159b0d2a-0cf0-42cb-a7f7-b93b7aec48c8" />





---

## 🚫 License
Open-source for educational and institutional use.

---
