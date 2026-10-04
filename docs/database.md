# Database Documentation

## Database Engine

**SQLite 3**
- Lightweight, serverless database
- File-based storage
- ACID compliant
- Suitable for prototypes and small applications

## Database Schema

### Table: users

Stores user account information.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    otp_secret TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Columns:**
- `id`: Auto-incrementing primary key
- `username`: Unique username for login
- `email`: Unique email address
- `password_hash`: bcrypt hashed password (never plaintext)
- `otp_secret`: Secret key for TOTP generation
- `created_at`: Account creation timestamp

**Constraints:**
- `username` must be unique
- `email` must be unique
- All fields are required (NOT NULL)

### Table: wallets

Stores wallet information for each user.

```sql
CREATE TABLE wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    balance REAL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

**Columns:**
- `id`: Auto-incrementing primary key
- `user_id`: Foreign key to users table (unique)
- `balance`: Current wallet balance (REAL/float)

**Constraints:**
- `user_id` must be unique (one wallet per user)
- `user_id` references `users.id`

**Relationships:**
- One-to-one with users table

### Table: transactions

Stores transaction history between users.

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    encrypted_note TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
```

**Columns:**
- `id`: Auto-incrementing primary key
- `sender_id`: Foreign key to users (sender)
- `receiver_id`: Foreign key to users (receiver)
- `amount`: Transaction amount (REAL/float)
- `encrypted_note`: Optional encrypted note (Fernet encrypted)
- `timestamp`: Transaction timestamp

**Constraints:**
- `sender_id` references `users.id`
- `receiver_id` references `users.id`
- `amount` must be positive (enforced by application logic)

**Relationships:**
- Many-to-one with users (sender)
- Many-to-one with users (receiver)

## Indexes

Performance optimization indexes:

```sql
CREATE INDEX idx_transactions_sender ON transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON transactions(receiver_id);
CREATE INDEX idx_wallets_user ON wallets(user_id);
```

## Database Operations

### Connection Management

Uses context manager for automatic connection handling:

```python
with db.get_connection() as conn:
    cursor = conn.cursor()
    # Execute queries
    # Auto-commit on success
    # Auto-rollback on error
```

### Transaction Safety

All money transfers use atomic transactions:

```python
with db.get_connection() as conn:
    cursor = conn.cursor()
    
    # Step 1: Deduct from sender
    cursor.execute("UPDATE wallets SET balance = balance - ? WHERE user_id = ?", 
                   (amount, sender_id))
    
    # Step 2: Add to receiver
    cursor.execute("UPDATE wallets SET balance = balance + ? WHERE user_id = ?", 
                   (amount, receiver_id))
    
    # Step 3: Record transaction
    cursor.execute("INSERT INTO transactions (...) VALUES (...)", 
                   (sender_id, receiver_id, amount, encrypted_note))
    
    # Auto-commit if all succeed, auto-rollback if any fail
```

### Query Types

**Parameterized Queries (SAFE)**
```python
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

**String Formatting (UNSAFE - NEVER USE)**
```python
# DON'T DO THIS - SQL INJECTION VULNERABILITY
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

## Data Types

| Column Type | SQLite Type | Python Type |
|-------------|-------------|-------------|
| id          | INTEGER     | int         |
| username    | TEXT        | str         |
| email       | TEXT        | str         |
| password_hash | TEXT      | str         |
| otp_secret  | TEXT        | str         |
| balance     | REAL        | float       |
| amount      | REAL        | float       |
| encrypted_note | TEXT     | str         |
| timestamp   | TIMESTAMP   | datetime    |

## Database File

**Location**: `ewallet.db` (in project root)

**Initialization**: Automatic on first run

**Backup**: Copy `ewallet.db` file

## Migration Notes

For production use, consider migrating to:
- **PostgreSQL**: Better concurrency, ACID compliance
- **MySQL**: Widely supported, good performance
- **MongoDB**: If document-based storage is needed

## Query Examples

### Get User by Username
```python
rows = db.execute_query(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```

### Get Wallet Balance
```python
rows = db.execute_query(
    "SELECT balance FROM wallets WHERE user_id = ?",
    (user_id,)
)
```

### Get Transaction History
```python
rows = db.execute_query(
    """
    SELECT * FROM transactions 
    WHERE sender_id = ? OR receiver_id = ? 
    ORDER BY timestamp DESC 
    LIMIT ?
    """,
    (user_id, user_id, limit)
)
```

### Create Wallet
```python
wallet_id = db.execute_insert(
    "INSERT INTO wallets (user_id, balance) VALUES (?, ?)",
    (user_id, initial_balance)
)
```

## Performance Considerations

- Indexes on frequently queried columns
- Connection pooling (for production)
- Query optimization for large datasets
- Regular VACUUM operations
- Consider read replicas for scaling
