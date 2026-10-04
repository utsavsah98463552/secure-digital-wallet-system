# System Architecture Blueprint

## 1. Overview

The Secure Digital Wallet System follows a **Service Layer Architecture** to ensure clean separation of concerns, testability, and adherence to SOLID design principles.

```
                      +-----------------------------+
                      |   Client / Browser / API    |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      | Presentation Layer (Routes) |
                      | auth / wallet / transaction |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |   Business Services Layer   |
                      | auth / wallet / tx / crypto |
                      +-------+-------------+-------+
                              |             |
             +----------------+             +----------------+
             v                                               v
+------------------------+                      +------------------------+
| Domain Models Layer    |                      |   Persistence Layer    |
| User / Wallet / Tx     |                      | SQLite / ACID Context  |
+------------------------+                      +------------------------+
```

## 2. Layer Responsibilities

### Presentation Layer (`routes/`)
- Parses incoming HTTP requests and validates parameters.
- Invokes appropriate service methods.
- Renders Jinja2 HTML templates or returns JSON responses.
- **Strict Rule:** No direct database queries or raw cryptographic hashing inside routes.

### Service Layer (`services/`)
- Encapsulates domain logic and business validation.
- Orchestrates multi-step operations (e.g., deducting from sender, adding to receiver, encrypting note).
- Guarantees financial invariants (e.g., non-negative balances).

### Domain Models (`models/`)
- Pure data representations:
  - `User`: user identity and authentication credentials.
  - `Wallet`: account balances associated with users.
  - `Transaction`: double-entry records linking sender, receiver, amount, and encrypted memo.

### Persistence Layer (`database.py`)
- Manages connection lifecycle and SQLite transaction contexts.
- Executes parameterized queries to defend against SQL Injection.

## 3. Cryptographic & Security Architecture

1. **Password Hashing**: `bcrypt` with dynamic salting.
2. **At-Rest Field Encryption**: `Fernet` (AES-128-CBC + HMAC-SHA256) for sensitive transaction notes.
3. **Multi-Factor Authentication**: RFC 6238 Time-based One-Time Passwords (`pyotp`).
4. **Session Security**: Enforced `HTTPOnly`, `SameSite=Lax`, and 30-minute idle expiration.
