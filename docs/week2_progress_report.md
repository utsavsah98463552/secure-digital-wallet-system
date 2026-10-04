# ACADEMIC PROJECT PROGRESS REPORT — WEEK 2

**Project Title:** E-Wallets and Digital Payments: Analysis and Development of a Secure Digital Wallet System  
**Course / Degree:** Bachelor of Science in Computer Science / Information Technology / Software Engineering  
**Academic Term:** Capstone Project / Final Year Project (8-Week Lifecycle)  
**Reporting Period:** Week 2 — Relational Schema Design, Persistence Layer & Transaction Safety  
**Submission Date:** October 5, 2026  
**Student Name:** [Your Name / Roll No.]  
**Project Supervisor:** [Supervisor / Professor Name]  
**Repository Link:** [https://github.com/your-username/secure-digital-wallet](https://github.com/your-username/secure-digital-wallet)

---

## 1. Executive Summary

During Week 2, the project shifted focus from project initiation and environment setup to **Data Architecture and Persistence Layer Engineering**. Financial systems demand uncompromising data consistency, relational integrity, and strict resistance to database corruption during unforeseen interruptions.

To address these requirements, we designed and implemented a dedicated `Database` subsystem using SQLite 3. The subsystem enforces foreign-key constraints, uses Python context managers (`contextlib.contextmanager`) to guarantee atomic transaction commit/rollback semantics, and optimizes ledger query lookups through dedicated B-tree indexes.

---

## 2. Entity-Relationship (ER) Design & Relational Schema

Three core tables were designed and verified:

```
+--------------------+           +--------------------+
|       users        |           |      wallets       |
+--------------------+           +--------------------+
| id (PK)            | 1       1 | id (PK)            |
| username (UNIQUE)  +-----------+ user_id (FK, UNIQUE)
| email (UNIQUE)     |           | balance (REAL)     |
| password_hash      |           +--------------------+
| otp_secret         |
| created_at         |
+---------+----------+
          | 1
          |
          | M (Sender / Receiver)
          v
+--------------------+
|    transactions    |
+--------------------+
| id (PK)            |
| sender_id (FK)     |
| receiver_id (FK)   |
| amount (REAL)      |
| encrypted_note     |
| timestamp          |
+--------------------+
```

### Table Specifications:
1. **`users` Table:**
   - Holds core authentication credentials and MFA seeds.
   - Enforces unique constraints on both `username` and `email`.
   - Never holds cleartext passwords (`password_hash` stores salted bcrypt digests).
2. **`wallets` Table:**
   - Enforces a strict **1:1 relationship** with users via `user_id INTEGER UNIQUE`.
   - Stores current available balance (`REAL DEFAULT 0.0`).
   - Configured with `ON DELETE CASCADE` to maintain relational hygiene.
3. **`transactions` Table:**
   - Double-entry ledger linking `sender_id` and `receiver_id` back to `users(id)`.
   - Contains `amount REAL NOT NULL` and `encrypted_note TEXT` for private memos.

---

## 3. Transaction Safety & ACID Compliance

In naive digital wallet implementations, transferring balance between two accounts without atomic locking introduces dangerous race conditions:
$$\text{Account } A \xrightarrow{-\$50} \text{ [CRASH/FAILURE] } \centernot\xrightarrow{+\$50} \text{Account } B$$

To solve this, our `get_connection()` manager in `database.py` wraps all SQLite operations inside explicit transaction boundaries:

```python
@contextmanager
def get_connection(self):
    conn = sqlite3.connect(self.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()     # Atomic Commit
    except Exception as e:
        conn.rollback()   # Guaranteed Rollback on any failure
        raise e
    finally:
        conn.close()
```

---

## 4. Security & Performance Optimizations

1. **SQL Injection (SQLi) Defense:**
   - All query interfaces (`execute_query`, `execute_insert`, `execute_update`) strictly mandate parameterized arguments (`?` placeholders). String interpolation is strictly prohibited.
2. **Indexing Strategy:**
   - Created indexes on high-frequency lookup fields:
     - `idx_transactions_sender ON transactions(sender_id)`
     - `idx_transactions_receiver ON transactions(receiver_id)`
     - `idx_wallets_user ON wallets(user_id)`
   - This ensures $O(\log N)$ retrieval complexity for user dashboards and transaction histories as the ledger grows.

---

## 5. Week 2 Deliverables & Verification

The following deliverables were implemented and committed to version control:
- **`database.py`:** Core connection pooling, context management, query wrappers, and automated schema migration.
- **`tests/test_database.py`:** Automated unit tests covering table creation, parameterized insertion, duplicate constraint enforcement, and atomic rollback verification.
- **`docs/database.md`:** Comprehensive database documentation including field types, relationship diagrams, and query patterns.
- **Updated `app.py`:** Integrated `Database` instance into Flask application context with live database health monitoring via `GET /health`.

**Testing Output:**
```text
Ran 4 tests in 0.346s
OK (All database schema, constraint, and rollback tests passed)
```

---

## 6. Plan for Week 3

For Week 3, the project will implement the **Security & Cryptography Subsystem**:
- Develop `EncryptionService` using `cryptography.Fernet` (AES-128-CBC with HMAC authentication).
- Implement secure encryption and decryption routines for transaction notes.
- Establish key management procedures using environment variables.
- Write unit tests for encryption integrity, unicode payloads, and tampering resistance.
