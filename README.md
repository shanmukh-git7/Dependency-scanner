# Dependency Vulnerability Scanner

A web-based security application for analyzing software dependency files, identifying potentially vulnerable dependencies, maintaining scan history, and generating security reports.

The project is designed around **dependency vulnerability management and software supply-chain security**, with support for multiple dependency-file formats and a FastAPI-based backend.

> **Project status:** Active development  
> **Primary language:** Python  
> **Backend:** FastAPI  
> **Database:** SQLite / SQLAlchemy

---

## Overview

Modern web applications depend heavily on third-party libraries and open-source packages. Vulnerable dependencies can introduce security risks such as remote code execution, injection vulnerabilities, insecure deserialization, denial-of-service conditions, and other attack vectors.

The Dependency Vulnerability Scanner provides a centralized interface where users can upload dependency files and perform automated dependency analysis.

The application provides:

- User authentication and authorization
- Dependency-file upload and analysis
- Multi-format dependency parsing
- Vulnerability identification
- Scan history
- PDF security reports
- Administrative functionality
- REST API endpoints through FastAPI

The project is being developed toward a more advanced vulnerability-intelligence architecture with **version-aware vulnerability matching and external vulnerability databases**.

---

## Key Features

### 🔐 Authentication & Authorization

- User registration
- User login
- JWT-based authentication
- Password recovery workflow
- Role-based access control
- Administrator functionality

### 📦 Dependency Analysis

The application currently accepts several dependency-file formats, including:

- `pom.xml`
- `package.json`
- `package-lock.json`
- `requirements.txt`
- `.lock`
- `.yaml`
- `.yml`

### 🔎 Vulnerability Detection

The current implementation performs dependency-name-based vulnerability identification against a local vulnerability dataset.

The vulnerability engine is planned for enhancement with:

- Version-aware matching
- CVE/GHSA identification
- CVSS-based severity
- Affected-version analysis
- Fixed-version recommendations
- External vulnerability intelligence sources

### 📊 Scan Management

Users can:

- Perform dependency scans
- View previous scans
- Delete scan records
- Review vulnerability details

### 📄 Security Reports

The application can generate PDF reports containing information such as:

- Scan date
- User
- Number of dependencies
- Number of identified vulnerabilities
- Vulnerability details
- Severity information

### 👨‍💻 Administrative Controls

Administrative functionality provides additional management capabilities for authorized users.

---

## System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Web Frontend      │
                    │ HTML / CSS / JS      │
                    └──────────┬───────────┘
                               │
                         REST API / HTTP
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI Backend  │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
      │ Authentication│ │ Dependency   │  │ Scan History │
      │ & Authorization│ │ Parser       │  │ & Reporting  │
      └─────────────┘  └──────┬───────┘  └──────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Vulnerability   │
                     │ Analysis Engine │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    SQLite DB    │
                     │   SQLAlchemy    │
                     └─────────────────┘
```

---

## How It Works

The general scanning workflow is:

```text
1. User authenticates
        ↓
2. Dependency file is uploaded
        ↓
3. File format is identified
        ↓
4. Appropriate parser extracts dependencies
        ↓
5. Dependencies are analyzed
        ↓
6. Potential vulnerabilities are identified
        ↓
7. Scan result is stored
        ↓
8. Results are displayed to the user
        ↓
9. Security report can be generated
```

---

## Supported File Formats

| Format | Purpose |
|---|---|
| `pom.xml` | Maven dependency analysis |
| `package.json` | Node.js dependency analysis |
| `package-lock.json` | Node.js lockfile analysis |
| `requirements.txt` | Python dependency analysis |
| `.lock` | Lock-file analysis |
| `.yaml` / `.yml` | YAML-based dependency information |

Support for additional dependency ecosystems and lockfile formats is planned.

---

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- lxml

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- SQLite
- SQLAlchemy ORM

### Security

- JWT authentication
- Password hashing
- Role-based authorization
- Dependency vulnerability analysis

### Reporting

- ReportLab
- PDF report generation

---

## Project Structure

```text
Dependency-scanner/
│
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routes/
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   └── scan_routes.py
│   │
│   ├── services/
│   │   ├── pom_parser.py
│   │   ├── report_generator.py
│   │   └── vulnerability_checker.py
│   │
│   └── utils/
│       ├── email_utils.py
│       └── pdf_generator.py
│
├── frontend/
│   ├── admin.html
│   ├── dashboard.html
│   ├── forgot-password.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── reset-password.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shanmukh-git7/Dependency-scanner.git
cd Dependency-scanner
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Do not commit credentials, API keys, passwords, or other secrets to the repository.

---

## Running the Application

Start the FastAPI development server:

```bash
uvicorn backend.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## API Capabilities

The backend provides functionality for:

- Authentication
- User registration
- Login
- Password recovery
- Dependency scanning
- Scan history
- Scan deletion
- PDF report generation
- Administrative operations

The API can be explored through the FastAPI Swagger interface.

---

## Security Considerations

Because this project itself is a security-oriented application, security is treated as an important part of its development.

Current security-related components include:

- JWT-based authentication
- Password hashing
- User authorization
- Role-based access control
- User-specific scan history
- Protected report access
- Environment-variable based configuration

Future security improvements include:

- Input validation hardening
- Upload size and content restrictions
- Dependency parser hardening
- Improved error handling
- Rate limiting
- Security headers
- Audit logging
- Vulnerability-source validation
- Automated security testing

---

## Current Limitations

The current vulnerability analysis engine is an early implementation.

Important limitations include:

- Vulnerability detection is currently based on a local vulnerability dataset.
- Dependency versions are not yet consistently preserved across all supported formats.
- Vulnerability matching is not yet fully version-aware.
- Vulnerability intelligence is not yet integrated into a comprehensive external database workflow.
- Some dependency formats use simplified parsing logic.

These limitations are intentionally documented because they define the next development stage of the project.

---

## Roadmap

### Phase 1 — Dependency Intelligence

- [ ] Normalize dependency representation
- [ ] Preserve package versions
- [ ] Improve Maven parsing
- [ ] Improve Python dependency parsing
- [ ] Improve Node.js dependency parsing

### Phase 2 — Vulnerability Intelligence

- [ ] Integrate OSV vulnerability intelligence
- [ ] Investigate NVD enrichment
- [ ] Implement CVE identification
- [ ] Implement affected-version matching
- [ ] Implement fixed-version detection
- [ ] Add CVSS information

### Phase 3 — Security Analysis

- [ ] Severity classification
- [ ] Risk prioritization
- [ ] Vulnerability deduplication
- [ ] Remediation recommendations
- [ ] Dependency risk scoring

### Phase 4 — Reporting & Visualization

- [ ] Improved security dashboard
- [ ] Vulnerability severity charts
- [ ] CVE-focused reports
- [ ] Remediation summaries
- [ ] Improved PDF reports

### Phase 5 — DevSecOps Integration

- [ ] GitHub repository scanning
- [ ] CI/CD integration
- [ ] Automated security checks
- [ ] Pull-request vulnerability reporting
- [ ] Security pipeline integration

### Phase 6 — Research Direction

- [ ] Dependency-risk prioritization
- [ ] Software supply-chain security research
- [ ] Vulnerability correlation
- [ ] Automated vulnerability intelligence
- [ ] Research-oriented evaluation datasets
- [ ] Detection accuracy evaluation

---

## Research Direction

This project is being developed beyond a basic dependency scanner toward a broader **software supply-chain security and vulnerability intelligence platform**.

Potential research areas include:

- Automated dependency vulnerability detection
- Software supply-chain security
- Vulnerability prioritization
- Dependency risk analysis
- Vulnerability intelligence correlation
- Automated remediation recommendation
- Security automation for DevSecOps

---

## Screenshots

Screenshots demonstrating the following application components will be added:

- Login
- Registration
- Dashboard
- Dependency upload
- Scan results
- Scan history
- Vulnerability details
- PDF security report
- Administration panel

---

## Future Vision

The long-term goal is to evolve the project from a basic dependency scanner into a **security intelligence platform capable of analyzing software dependencies, correlating vulnerability information, prioritizing risk, and providing actionable remediation guidance.**

The project will also serve as a practical research platform for exploring software supply-chain security and automated vulnerability management.

---

## Contributing

Contributions, security research ideas, bug reports, and improvement suggestions are welcome.

Before contributing, please review the project documentation and security considerations.

---

## License

This project is currently under active development.

A formal open-source license will be added before the project is released as a finalized public security tool.
