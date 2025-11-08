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
git clone <your-repo-url>
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

## 👨‍💻 Author
**Developed by:** Pratheek J Gowda  
**Institution:** PES University  
**Course:** UE23CS351A - DBMS Mini Project  

---

## 🚫 License
Open-source for educational and institutional use.

---