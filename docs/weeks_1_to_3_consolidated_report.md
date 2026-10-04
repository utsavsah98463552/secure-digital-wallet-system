# ACADEMIC PROGRESS REPORT (WEEKS 1 — 3 CONSOLIDATED)

**Project Title:** E-Wallets and Digital Payments: Analysis and Development of a Secure Digital Wallet System  
**Course / Degree:** Bachelor of Science in Computer Science / Information Technology / Software Engineering  
**Academic Term:** Capstone Project / Final Year Project (8-Week Lifecycle)  
**Reporting Period:** Weeks 1 to 3 — Initiation, Database Architecture & Cryptography Subsystem  
**Submission Date:** October 5, 2026  
**Student Name:** Utsav Sah  
**Project Supervisor:** [Supervisor / Professor Name]  
**Repository:** [https://github.com/utsavsah98463552/secure-digital-wallet-system](https://github.com/utsavsah98463552/secure-digital-wallet-system)

---

## 1. Executive Summary

Digital payment applications and electronic wallets represent the backbone of today's cashless economies. However, their proliferation exposes users and institutions to severe attack vectors, including credential breaches, non-atomic ledger inconsistencies, and private transaction leakages.

This capstone project is an engineering analysis and progressive development of a **Secure Digital Wallet System** patterned after modern defense-in-depth principles. Over the first three weeks of our planned 8-week software development lifecycle, we have transitioned from requirement formulation to data layer persistence and cryptographic engineering:
- **Week 1:** Project Initiation, SRS Specification, and Multi-Environment Architecture Bootstrap.
- **Week 2:** Relational Database Modeling with SQLite, Atomic Commit/Rollback Context Management, and Index Optimization.
- **Week 3:** Security and Cryptography Subsystem Engineering utilizing Fernet (AES-128-CBC + HMAC-SHA256) for data at rest and adaptive `bcrypt` for credential salting.

All 15 automated unit tests are passing, and progressive commits have been staged and pushed to the remote repository.

---

## 2. 8-Week SDLC Milestone Schedule

| Week | Focus / Phase | Deliverable | Status |
| :---: | :--- | :--- | :---: |
| **Week 1** | **Project Initiation & Foundation** | Requirements SRS, System Architecture Blueprint, Multi-Env Config (`config.py`), Base Flask Factory | ✅ **Done** |
| **Week 2** | **Database Schema & Persistence** | Relational SQLite Schema (`users`, `wallets`, `transactions`), Context Managers, Indexing | ✅ **Done** |
| **Week 3** | **Cryptography Subsystem** | `Fernet` Key Management, Transaction Note Encryption/Decryption, `bcrypt` Hashing Utilities | ✅ **Done** |
| **Week 4** | **Authentication & 2FA (TOTP)** | User Registration, Credential Verification, Time-based OTP via `pyotp`, Session Security | ⏳ Planned |
| **Week 5** | **Wallet Core & Balance Management** | Auto Wallet Provisioning, Balance Inquiries, Fund Loading Service & Unit Tests | ⏳ Planned |
| **Week 6** | **Peer-to-Peer Transfer Engine** | Atomic Transaction Processing, ACID Double-Entry Ledger, Rollback Verification | ⏳ Planned |
| **Week 7** | **Presentation Layer & UI** | Jinja2 Templates, Bootstrap 5 Dashboard, Transfer Interfaces, Audit History View | ⏳ Planned |
| **Week 8** | **System Testing, Security Audit & Final Report** | Test Discovery Suite (`unittest`), SQLi/CSRF/Timing Verification, Final Documentation | ⏳ Planned |

---

## 3. Detailed Weekly Progress Breakdown

### 3.1 Week 1: Initiation, Requirements & Environment Bootstrap
- **Formal Requirements Specification (SRS):** Defined 7 core functional requirements (FR1–FR7) covering user registration, two-factor authentication, wallet lifecycle, balance loading, P2P transfers, encrypted memos, and transaction auditing.
- **4-Tier Service Layer Architecture:** Segregated the application into Presentation (`routes/`), Domain Business Logic (`services/`), Entities (`models/`), and Data Storage (`database.py`).
- **Configuration Management:** Implemented `config.py` defining `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig` with session protections (`HTTPOnly`, 30-min expiration).
- **Verification:** Initialized Git repository, verified virtual environment, and built `tests/test_config.py` (4 unit tests passing).

### 3.2 Week 2: Relational Schema & Persistence Layer
- **Schema Engineering:** Designed three relational entities:
  - `users`: stores `id`, unique `username`, unique `email`, salted `password_hash`, and MFA `otp_secret`.
  - `wallets`: enforces a strict 1:1 relationship with `users` (`user_id UNIQUE`) and holds float balance.
  - `transactions`: double-entry financial ledger recording `sender_id`, `receiver_id`, `amount`, and `encrypted_note`.
- **ACID Transaction & Rollback Safety:** Implemented `Database.get_connection()` using Python context managers. Any unhandled exception during ledger operations triggers an immediate `conn.rollback()`, preventing orphaned balance state.
- **Performance Optimization:** Implemented B-tree indexes (`idx_transactions_sender`, `idx_transactions_receiver`, `idx_wallets_user`) to guarantee $O(\log N)$ transaction history lookups.
- **Verification:** Built `tests/test_database.py` (4 unit tests passing, verifying constraints and automatic rollbacks).

### 3.3 Week 3: Security & Cryptography Subsystem
- **Symmetric Data-at-Rest Protection:** Implemented `EncryptionService` utilizing `cryptography.fernet.Fernet`:
  - Enforces AES-128 in CBC mode with PKCS7 padding.
  - Generates unique 128-bit IVs per encryption operation.
  - Authenticates tokens using HMAC-SHA256 to immediately detect manual or malicious database tampering.
- **Adaptive Password Hashing:** Formulated credential storage policies using `bcrypt`. Dynamically salts passwords with a computational cost factor to resist GPU/ASIC rainbow-table attacks.
- **Verification:** Built `tests/test_encryption.py` (7 unit tests passing, covering encryption round-trips, unicode/emoji handling, empty string sanitization, and cryptographic tamper detection).

---

## 4. Current Verification & System Health Metrics

Running the automated test discovery across the entire repository:
```text
$ python -m unittest discover tests
Ran 15 tests in 1.580s
OK
```

Querying the application health endpoint (`GET /health`):
```json
{
  "cryptography": {
    "algorithm": "Fernet (AES-128-CBC + HMAC-SHA256)",
    "status": "operational"
  },
  "database": "connected",
  "security": {
    "session_httponly": true,
    "session_lifetime_sec": 1800
  },
  "status": "healthy"
}
```

---

## 5. Plan for Week 4

During Week 4, development will focus on the **User Authentication & Multi-Factor Authentication (2FA)** subsystem:
1. Implement `models/user.py` data structure.
2. Build `AuthService` in `services/auth_service.py` to handle registration, password hashing with `bcrypt`, and credential matching.
3. Implement RFC 6238 Time-based One-Time Passwords (TOTP) with `pyotp` (30-second time step).
4. Implement session management and login state handling.
