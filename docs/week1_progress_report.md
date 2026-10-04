# ACADEMIC PROJECT PROGRESS REPORT — WEEK 1

**Project Title:** E-Wallets and Digital Payments: Analysis and Development of a Secure Digital Wallet System  
**Course / Degree:** Bachelor of Science in Computer Science / Information Technology / Software Engineering  
**Academic Term:** Capstone Project / Final Year Project (8-Week Lifecycle)  
**Reporting Period:** Week 1 — Project Initiation, Requirement Engineering & Architecture Setup  
**Submission Date:** October 5, 2026  
**Student Name:** [Your Name / Roll No.]  
**Project Supervisor:** [Supervisor / Professor Name]  
**Repository Link:** [https://github.com/your-username/secure-digital-wallet](https://github.com/your-username/secure-digital-wallet)

---

## 1. Executive Summary & Project Background

With the exponential surge in cashless economies and digital payments, digital wallet systems (e-wallets) have become critical financial infrastructure. However, digital transactions introduce severe security challenges, including identity spoofing, credential theft, transaction interception, and unauthorized fund manipulation.

This project focuses on the **in-depth security analysis and development of a robust prototype Digital Wallet System**. The system is engineered from the ground up prioritizing financial data integrity, multi-factor authentication (MFA/TOTP), at-rest data encryption, and atomic transaction handling following ACID database principles. The prototype is developed using Python, the Flask web framework, SQLite with parameterized execution, bcrypt for password hashing, and Fernet (symmetric cryptography) for sensitive payload encryption.

---

## 2. Problem Statement & Motivation

Traditional web-based financial prototypes often suffer from critical vulnerabilities:
1. **Insecure Authentication**: Weak password hashing algorithms (e.g., MD5/SHA1) and absence of multi-factor authentication, making accounts vulnerable to credential stuffing and brute-force attacks.
2. **Transaction Integrity Vulnerabilities**: Non-atomic database updates where funds are deducted from the sender but fail to reach the recipient during unexpected network or system crashes.
3. **Plaintext Financial Data Exposure**: Storing transaction memos and financial metadata as cleartext in databases, leaving sensitive financial memos vulnerable to database leakages.
4. **Injection Attacks**: Vulnerability to SQL Injection (SQLi) when queries concatenate raw user input.

**Project Motivation:** To build an educational, production-patterned e-wallet prototype that explicitly demonstrates how modern security layers (2FA, salted bcrypt, Fernet encryption, and atomic transactions) prevent these real-world fintech vulnerabilities.

---

## 3. Project Objectives & Scope

### 3.1 Primary Objectives
- **Secure Authentication Layer:** Implement salted, adaptive password hashing (bcrypt) and Time-based One-Time Password (TOTP) two-factor authentication.
- **Account & Ledger Management:** Design a double-entry style digital ledger enabling balance initialization, deposits, and real-time balance inquiries.
- **Atomic Peer-to-Peer Transfer Engine:** Develop an isolated transaction service executing safe money transfers with strict atomic consistency (all-or-nothing rollback mechanisms).
- **Cryptographic Protection of Transaction Payloads:** Implement AES-128-CBC/HMAC (Fernet) symmetric encryption to safeguard private transaction notes at rest.
- **Defensive Web Architecture:** Adopt Service-Oriented Layering (Routes $\to$ Services $\to$ Models $\to$ DB), strict parameterized SQL queries, secure HTTP session cookies, and input validation.

### 3.2 Scope Boundary (8-Week Academic Project)
- **In-Scope:**
  - Single-currency prototype (USD/NPR/Default credits).
  - P2P user-to-user transfers.
  - TOTP 2FA via authenticator-compatible algorithms.
  - End-to-end audit history with decrypted note retrieval for authorized parties.
  - Unit and integration testing suite covering security, wallet, and transaction logic.
- **Out-of-Scope (Deliberately deferred for future research):**
  - External banking API integration (Plaid/Stripe/ACH).
  - Multi-currency forex conversion.
  - Distributed database clustering (prototype utilizes SQLite with transactional locking).

---

## 4. Software Requirements Specification (SRS)

### 4.1 Functional Requirements (FR)
- **FR1 — User Registration & Verification:** System must allow new users to register with a unique username, valid email, and minimum 8-character password. Upon registration, a unique 160-bit TOTP secret key must be generated.
- **FR2 — Multi-Factor Authentication (MFA):** User login must require two factors: primary credentials (username + password) followed by a valid 6-digit TOTP code with a 30-second validity window.
- **FR3 — Wallet Lifecycle:** Every verified user account must automatically provision an associated wallet entity with an initial balance of $0.00$.
- **FR4 — Balance Addition (Mock Gateway):** Users must be able to add simulated funds to their personal wallet balance with positive-amount validation.
- **FR5 — P2P Transfers:** Users must be able to transfer funds to any other registered user by username. Transfers must fail if sender balance is insufficient or if sender equals recipient.
- **FR6 — Encrypted Transaction Notes:** Senders may attach a private transaction note. The system must encrypt this note using Fernet before writing to the database, and only decrypt it when rendering the authorized history view.
- **FR7 — Transaction Audit Log:** Both sender and receiver must be able to view their chronological transaction history with timestamps, participant names, and decrypted memos.

### 4.2 Non-Functional Requirements (NFR)
- **NFR1 — Confidentiality & Cryptography:** Zero plaintext passwords stored. Symmetrical encryption keys must be managed via environment variables.
- **NFR2 — Transactional Atomicity (ACID):** Database updates involving both accounts and the ledger record must execute within an atomic transaction boundary. Any failure must trigger an immediate rollback.
- **NFR3 — SQL Injection Immunity:** 100% of database interactions must use parameterized statements (`?` placeholders).
- **NFR4 — Session Security:** Sessions must enforce `HTTPOnly`, `SameSite=Lax`, and a 30-minute idle expiration window.
- **NFR5 — Maintainability & Modularity:** Adherence to SOLID design principles using a distinct Service Layer pattern separating presentation, domain rules, and data access.

---

## 5. Technology Stack & Justification

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.11+ | High readability, robust standard cryptographic libraries, native support for modern typing and context managers. |
| **Web Framework** | Flask 3.0.0 | Lightweight, unopinionated microframework allowing granular architectural control over routing, session handling, and security middlewares without ORM bloat. |
| **Database Engine** | SQLite 3 | Zero-configuration, file-based relational database supporting full ACID transactions, foreign key constraints, and connection pooling. |
| **Password Hashing** | `bcrypt` (4.1.2) | Industry standard adaptive hashing function with built-in per-password salt generation, designed to be computationally resistant to GPU brute-force attacks. |
| **Payload Encryption** | `cryptography.Fernet` | High-level symmetric encryption primitive implementing AES-128 in CBC mode with PKCS7 padding and HMAC-SHA256 authentication, preventing tampering. |
| **Two-Factor Auth** | `pyotp` (2.9.0) | RFC 6238 compliant Time-Based One-Time Password algorithm compatible with standard authenticator applications. |
| **Frontend UI** | HTML5 / Bootstrap 5 / CSS3 | Clean, responsive, mobile-friendly interface for dashboard, forms, and transaction tables without complex JavaScript build pipelines. |
| **Version Control** | Git & GitHub | Distributed version control tracking progressive, incremental weekly development milestones. |

---

## 6. 8-Week Work Breakdown Structure (SDLC Roadmap)

| Week | Milestone / Focus | Key Deliverables & Expected Commits | Status |
| :--- | :--- | :--- | :--- |
| **Week 1** | **Project Initiation, SRS & Environment Setup** | Requirements spec, architecture blueprint, Git repo initialization, virtual environment, `requirements.txt`, `.gitignore`, configuration manager (`config.py`), base health endpoint. | **COMPLETED** |
| **Week 2** | **Database Schema Design & Persistence Layer** | Relational schema definition (`users`, `wallets`, `transactions`), index strategy, `database.py` with thread-safe context managers, rollback handling, and DB init scripts. | Planned |
| **Week 3** | **Security & Cryptography Foundation** | `encryption_service.py` (Fernet key generation, encryption/decryption routines), hashing utilities with `bcrypt`, mock key management tests. | Planned |
| **Week 4** | **User Authentication & Two-Factor Auth (TOTP)** | `models/user.py`, `auth_service.py`, registration logic, credential validation, TOTP generation & verification (`pyotp`), session lifecycle. | Planned |
| **Week 5** | **Wallet Engine & Balance Operations** | `models/wallet.py`, `wallet_service.py`, automated wallet creation upon user signup, balance inquiry, deposit/fund addition logic, unit test suite. | Planned |
| **Week 6** | **Peer-to-Peer Transfer Engine & ACID Safety** | `models/transaction.py`, `transaction_service.py`, atomic double-entry balance adjustment, rollback validation under stress, encrypted memo storage. | Planned |
| **Week 7** | **Presentation Layer & Frontend UI** | Flask blueprints (`auth_routes.py`, `wallet_routes.py`, `transaction_routes.py`), Bootstrap 5 templates (`login`, `register`, `dashboard`, `send`, `history`), Flash alerts. | Planned |
| **Week 8** | **Comprehensive Testing, Security Audit & Final Report** | Full test discovery suite (`unittest`), edge-case validation, manual security testing (SQLi/XSS/Brute-force verification), final thesis/documentation. | Planned |

---

## 7. Week 1 Accomplishments (Current Progress)

During this initial development cycle, the following milestones have been achieved:
1. **Requirements & Scope Finalization:** Formulated the complete Functional and Non-Functional specifications, bounding the 8-week prototype scope.
2. **Architecture Blueprinting:** Defined the 4-tier Service Layer Architecture:
   - Presentation Tier (`routes/` & `templates/`)
   - Business Logic Tier (`services/`)
   - Domain Entity Tier (`models/`)
   - Data Access Tier (`database.py`)
3. **Repository & Version Control Setup:**
   - Initialized a clean Git repository with standard branches.
   - Configured `.gitignore` to prevent database files (`*.db`), secrets (`.env`), and Python bytecode (`__pycache__`) from entering source control.
4. **Environment & Dependency Bootstrap:**
   - Established isolated Python 3.11 virtual environment.
   - Pinned core dependencies (`Flask`, `bcrypt`, `cryptography`, `pyotp`).
5. **Configuration Subsystem (`config.py`):**
   - Implemented environment-specific configurations: `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig` with fallback keys and configurable session parameters.
6. **Application Factory Verification:**
   - Created the baseline Flask application factory in `app.py` and verified HTTP server startup on `127.0.0.1:5000`.

---

## 8. Plan for Week 2

For the upcoming week, development will focus on the **Persistence and Data Modeling Layer**:
- Define SQLite relational schema for `users`, `wallets`, and `transactions` tables with strict foreign keys.
- Write the `Database` class in `database.py` utilizing Python's `contextlib.contextmanager` for automatic commit/rollback.
- Implement database indexing on foreign keys (`sender_id`, `receiver_id`, `user_id`) to optimize transaction query performance.
- Write schema initialization scripts and verify automated table creation on clean boot.

---

## 9. Conclusion & Supervisor Feedback Request

Week 1 has successfully established the project roadmap, security guidelines, and technical infrastructure. The system is positioned for clean database layer development in Week 2.

**Supervisor Review Notes:**
- *Supervisor Signature:* ___________________________
- *Date:* ___________________________
- *Feedback / Recommendations:*
