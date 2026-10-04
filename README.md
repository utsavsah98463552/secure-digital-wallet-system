# Secure Digital Wallet System

An academic capstone project focused on the **Analysis and Development of a Secure Digital Wallet System**, implementing defense-in-depth security principles for digital payments.

Developed progressively across an **8-Week Software Development Lifecycle (SDLC)**.

---

## 📅 8-Week Progressive Development Roadmap

| Week | Focus / Phase | Deliverable | Status |
| :---: | :--- | :--- | :---: |
| **Week 1** | **Project Initiation & Foundation** | Requirements SRS, System Architecture Blueprint, Environment Configuration, Base Flask Factory | ✅ **Done** |
| **Week 2** | **Database Schema & Persistence** | Relational SQLite Schema (`users`, `wallets`, `transactions`), Context Managers, Indexing | ✅ **Done** |
| **Week 3** | **Cryptography Subsystem** | `Fernet` Key Management, Transaction Note Encryption/Decryption, `bcrypt` Hashing Utilities | ✅ **Done** |
| **Week 4** | **Authentication & 2FA (TOTP)** | User Registration, Credential Verification, Time-based OTP via `pyotp`, Session Security | ⏳ Planned |
| **Week 5** | **Wallet Core & Balance Management** | Auto Wallet Provisioning, Balance Inquiries, Fund Loading Service & Unit Tests | ⏳ Planned |
| **Week 6** | **Peer-to-Peer Transfer Engine** | Atomic Transaction Processing, ACID Double-Entry Ledger, Rollback Verification | ⏳ Planned |
| **Week 7** | **Presentation Layer & UI** | Jinja2 Templates, Bootstrap 5 Dashboard, Transfer Interfaces, Audit History View | ⏳ Planned |
| **Week 8** | **System Testing, Security Audit & Final Report** | Test Discovery Suite (`unittest`), SQLi/CSRF/Timing Verification, Final Documentation | ⏳ Planned |

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11+, Flask 3.0.0
- **Database:** SQLite 3 (ACID-compliant with parameterized execution)
- **Security & Cryptography:** `bcrypt`, `cryptography.Fernet`, `pyotp`
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Testing:** Python `unittest`

---

## 🚀 Week 1 Quick Start & Verification

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/secure-digital-wallet.git
cd secure-digital-wallet
```

### 2. Create and Activate Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Week 1 Unit Tests
```bash
python -m unittest discover tests
```

### 5. Launch the Development Server
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to verify the health status endpoint.

---

## 📂 Repository Structure

```
secure-digital-wallet/
├── app.py                  # Application factory entry point
├── config.py               # Environment configurations (Dev / Test / Prod)
├── requirements.txt        # Pinned project dependencies
├── .gitignore              # Git exclusion rules
├── models/                 # Domain entities (User, Wallet, Transaction)
├── services/               # Business logic services
├── routes/                 # HTTP controllers and blueprints
├── templates/              # Jinja2 HTML templates
├── static/                 # Static assets (CSS, JS, images)
├── tests/                  # Automated test suite
└── docs/                   # Architectural blueprints & weekly reports
    ├── architecture.md
    └── week1_progress_report.md
```

---

## 📄 Documentation

- [System Architecture Blueprint](docs/architecture.md)
- [Database Architecture & Schema](docs/database.md)
- [Security & Cryptography Specification](docs/security.md)
- [Week 1 Progress Report](docs/week1_progress_report.md)
- [Week 2 Progress Report](docs/week2_progress_report.md)
- [Week 3 Progress Report](docs/week3_progress_report.md)
