# Dependency Scanner

A full-stack web application designed to scan project dependency files (`pom.xml`, `package.json`, `requirements.txt`) for potential vulnerabilities. The project features a robust FastAPI backend with secure authentication and a dynamic, cyber-security-themed frontend.

## 🚀 Features

- **Multi-Format Scanning:** Upload and analyze `pom.xml`, `package.json`, and `requirements.txt` files to identify dependency-related vulnerabilities.
- **Secure Authentication:** Complete user management system with JWT-based authentication, user registration, login, and secure password reset functionalities.
- **Interactive Dashboard:** User-friendly interface for uploading dependency files and visualizing scan results in real-time.
- **Admin Panel:** Administrative controls to monitor users, manage activity, and oversee system operations.
- **Detailed Reporting:** Generates downloadable professional vulnerability reports in PDF format.
- **Cyber-Themed UI:** A sleek, fully responsive front-end designed with modern cyber-security aesthetics including glassmorphism and dynamic elements.

## 🛠️ Technology Stack

**Backend:**
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens), `python-jose`, `passlib`
- **Other Tools:** `uvicorn`, `python-multipart`, `fpdf` (Reporting), `lxml`

**Frontend:**
- **Core:** HTML5, Vanilla JavaScript, CSS3
- **Design:** Custom Cyber Security Theme

## 📁 Project Structure

```
Application/
├── backend/                # FastAPI backend code
│   ├── main.py             # App entry point
│   ├── auth.py             # Authentication logic
│   ├── database.py         # DB connection setup
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic schemas for data validation
│   ├── routes/             # API routing modules
│   ├── services/           # Business logic and scanning engines
│   └── utils/              # Helper utilities
├── frontend/               # User interface files
│   ├── index.html          # Landing page
│   ├── login.html          # Authentication pages
│   ├── register.html
│   ├── dashboard.html      # Main scanning dashboard
│   ├── admin.html          # Administration view
│   ├── css/                # Stylesheets (Cyber Theme)
│   └── js/                 # Frontend interactivity
├── reports/                # Generated vulnerability reports
├── requirements.txt        # Python dependencies
└── ...
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   Navigate into your project folder.
   
2. **Set up a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database migrations:**
   (If applicable, run your database setup or let SQLAlchemy engine create tables on run if configured to do so).
   ```bash
   python migrate_db.py
   ```

5. **Start the Backend Server:**
   ```bash
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.

6. **Serve the Frontend:**
   Use any basic HTTP server to serve the frontend files to avoid CORS or fetch issues.
   ```bash
   # From the `frontend` directory
   python -m http.server 3000
   ```
   Open `http://localhost:3000` in your web browser.

## 🛡️ Usage
1. Register a new user account or log in with an existing account.
2. Navigate to the Dashboard.
3. Click on the scan section to upload your dependency file (`pom.xml`, `package.json`, or `requirements.txt`).
4. Wait for the engine to parse the file and return any potential vulnerabilities.
5. Export the summarized scan results using the PDF report feature if needed.

## 🤝 Contributing
Contributions are always welcome! Feel free to open an issue or submit a pull request for new features, bug fixes, or enhancements.
