# Security Documentation

## Security Features

### 1. Password Security

#### Hashing Algorithm
- **Algorithm**: bcrypt
- **Work Factor**: Default (automatically adjusted)
- **Salt**: Unique per password, automatically generated

#### Implementation
```python
# Password hashing
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Password verification
bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
```

#### Rules
- Minimum password length: 8 characters
- Passwords are never stored in plaintext
- Passwords are never logged or displayed

### 2. Data Encryption

#### Encryption Algorithm
- **Algorithm**: Fernet (AES-128 in CBC mode with HMAC)
- **Key Size**: 256 bits
- **Use Case**: Transaction notes

#### Implementation
```python
# Encryption
cipher = Fernet(encryption_key)
encrypted_data = cipher.encrypt(data.encode())

# Decryption
decrypted_data = cipher.decrypt(encrypted_data).decode()
```

#### Key Management
- Encryption key stored in environment variable
- Auto-generated if not provided
- Never hardcoded in source code

### 3. Two-Factor Authentication (2FA)

#### Implementation
- **Type**: Time-based One-Time Password (TOTP)
- **Algorithm**: HMAC-SHA1
- **Time Step**: 30 seconds
- **Validation Window**: ±1 time step

#### Flow
1. User registers → OTP secret generated
2. User logs in → Enters username + password
3. System validates credentials
4. User generates OTP using secret
5. System verifies OTP
6. Access granted

### 4. Session Security

#### Configuration
- `SESSION_COOKIE_SECURE`: True (HTTPS only in production)
- `SESSION_COOKIE_HTTPONLY`: True (prevents XSS)
- `SESSION_COOKIE_SAMESITE`: 'Lax' (prevents CSRF)
- `PERMANENT_SESSION_LIFETIME`: 1800 seconds (30 minutes)

### 5. SQL Injection Prevention

#### Parameterized Queries
All database queries use parameterized statements:

```python
# SAFE - Parameterized query
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# UNSAFE - String concatenation (NEVER DO THIS)
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

### 6. Input Validation

#### User Registration
- Username: Required, unique
- Email: Required, unique, valid format
- Password: Minimum 8 characters

#### Transactions
- Amount: Must be positive
- Sender/Receiver: Must exist and be different
- Balance: Validated before transfer

### 7. Error Handling

#### Security Principles
- Never expose internal errors to users
- Log errors securely (no sensitive data)
- Generic error messages for authentication failures
- Specific validation errors for user input

### 8. Database Security

#### Atomic Transactions
All money transfers use database transactions:
```python
with db.get_connection() as conn:
    # Deduct from sender
    # Add to receiver
    # Record transaction
    # Commit or rollback
```

#### Indexes
- Indexed columns for performance
- No sensitive data in indexes

### 9. Production Security Checklist

- [ ] Set `SECRET_KEY` environment variable
- [ ] Set `ENCRYPTION_KEY` environment variable
- [ ] Enable HTTPS
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Disable debug mode
- [ ] Implement rate limiting
- [ ] Add CORS protection
- [ ] Implement request logging
- [ ] Set up monitoring and alerts
- [ ] Regular security audits

### 10. Known Limitations

This is a **prototype system** with the following limitations:

- No rate limiting (vulnerable to brute force)
- No email verification
- No password reset functionality
- No account lockout after failed attempts
- No audit logging
- No IP-based restrictions
- SQLite (not suitable for production scale)

### 11. Security Best Practices

#### For Developers
- Never commit secrets to version control
- Use environment variables for sensitive data
- Always validate user input
- Use parameterized queries
- Keep dependencies updated
- Follow principle of least privilege

#### For Users
- Use strong, unique passwords
- Keep OTP secret secure
- Log out after use
- Don't share credentials
- Report suspicious activity
