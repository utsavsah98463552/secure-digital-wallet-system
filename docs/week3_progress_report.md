# ACADEMIC PROJECT PROGRESS REPORT — WEEK 3

**Project Title:** E-Wallets and Digital Payments: Analysis and Development of a Secure Digital Wallet System  
**Course / Degree:** Bachelor of Science in Computer Science / Information Technology / Software Engineering  
**Academic Term:** Capstone Project / Final Year Project (8-Week Lifecycle)  
**Reporting Period:** Week 3 — Cryptography Subsystem, Field-Level Encryption & Password Security Engineering  
**Submission Date:** October 5, 2026  
**Student Name:** Utsav Sah  
**Project Supervisor:** [Supervisor / Professor Name]  
**Repository Link:** [https://github.com/utsavsah98463552/secure-digital-wallet-system](https://github.com/utsavsah98463552/secure-digital-wallet-system)

---

## 1. Executive Summary

During Week 3, the project developed the **Security and Cryptography Subsystem**. In modern financial architectures, securing data at rest is a regulatory and defensive imperative. Cleartext storage of transaction memos and user notes exposes sensitive financial habits and metadata to insider threats, unauthorized read access, or physical database dump leaks.

In this phase, we implemented a dedicated `EncryptionService` utilizing the **Fernet symmetric cryptographic specification** (AES-128 in CBC mode with PKCS7 padding, combined with HMAC-SHA256 for message authentication). Furthermore, we analyzed and verified our credential protection layer based on the adaptive, memory-hard `bcrypt` hashing algorithm.

---

## 2. Cryptographic Architecture & Fernet Specification

### Why Fernet?
Rather than rolling a custom encryption primitive (which frequently introduces subtle implementation vulnerabilities such as Padding Oracle attacks or IV reuse), our subsystem utilizes `cryptography.fernet.Fernet`.

Fernet guarantees that data encrypted cannot be read or altered without the 256-bit symmetric key:
1. **Confidentiality:** Uses **AES-128-CBC** encryption with a cryptographically secure 128-bit Initialization Vector (IV) generated uniquely for every encryption operation.
2. **Authenticity & Integrity:** Generates an **HMAC-SHA256** signature over the entire ciphertext and metadata using a separate 128-bit signing subkey. Any manual or malicious bit modification triggers an immediate `InvalidToken` rejection before decryption is attempted.
3. **Replay Protection:** Encodes a 64-bit UTC timestamp in the header to allow optional expiration TTLs.

```
+---------------------------------------------------------------------------------+
|                               Fernet Token Format                               |
+-----------+--------------------+---------------------+------------+-------------+
|  Version  | Timestamp (64-bit) | IV Vector (128-bit) | Ciphertext | HMAC (256b) |
|  (1 byte) |                    |                     | (Variable) |             |
+-----------+--------------------+---------------------+------------+-------------+
```

---

## 3. Password Security: Adaptive bcrypt Hashing

In compliance with modern cryptographic guidelines (OWASP / NIST):
- General-purpose cryptographic hash functions (such as MD5, SHA-1, or plain SHA-256) are **unsuitable** for password hashing because high-throughput GPUs and ASICs can compute billions of candidate hashes per second.
- We utilize `bcrypt`, which is based on the Blowfish block cipher and incorporates a tunable work factor (cost parameter) and automatic 128-bit random salting:
  $$\text{Hash} = \text{bcrypt}(\text{Password}, \text{Salt}, \text{Cost})$$
- Even if two users choose identical passwords, their resulting hashes are completely distinct, rendering precomputed Rainbow Table attacks computationally useless.

---

## 4. `EncryptionService` Implementation Highlights

The `EncryptionService` class (`services/encryption_service.py`) encapsulates all symmetric operations cleanly away from presentation routes and database schemas:
- Sanitizes incoming payload types, handling `None` and empty string edge cases gracefully.
- Converts Unicode strings (including emojis and non-Latin character sets) into UTF-8 byte streams before encryption.
- Encodes output ciphertexts in URL-safe base64 formatting, ensuring seamless storage within SQLite `TEXT` columns and JSON APIs.

---

## 5. Automated Verification & Testing

A comprehensive unit test suite (`tests/test_encryption.py`) was developed and executed:
1. **Round-Trip Fidelity:** Tested encryption and decryption of financial memo strings.
2. **Boundary Testing:** Handled empty strings and `None` parameters without crashing.
3. **Unicode & Non-ASCII Testing:** Verified encryption of multilingual messages and emojis (e.g. `Payment for Momo Lunch 🥟`).
4. **Tamper Detection Test:** Intentionally mutated a byte in the ciphertext; confirmed that Fernet caught the tampering and raised `InvalidToken`.
5. **bcrypt Hashing & Verification Test:** Confirmed dynamic salting and password verification.

**Test Results:**
```text
Ran 7 tests in 2.069s
OK (All cryptography and hashing unit tests passed)
```

---

## 6. Cumulative Progress Summary (Weeks 1 — 3)

| Component | Status | Details |
| :--- | :---: | :--- |
| **Week 1: Initiation & Architecture** | Complete | SRS, 4-tier Service Layer, `config.py`, base Flask factory. |
| **Week 2: Database Persistence** | Complete | SQLite schema (`users`, `wallets`, `transactions`), context managers, ACID rollback. |
| **Week 3: Security & Cryptography** | Complete | `EncryptionService` (Fernet AES-128/HMAC), `bcrypt` salting verification, test suite. |

---

## 7. Plan for Week 4

For Week 4, the project will implement the **User Authentication & Multi-Factor Authentication (TOTP)** system:
- Implement `models/user.py` domain entity.
- Develop `AuthService` (`services/auth_service.py`) handling registration, credential validation, and password hashing.
- Integrate Time-based One-Time Passwords (`pyotp`) for 2FA.
- Configure secure session cookies (`HTTPOnly`, 30-minute timeout).
