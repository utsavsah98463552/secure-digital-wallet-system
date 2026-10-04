from cryptography.fernet import Fernet

class EncryptionService:
    """Symmetric encryption service utilizing Fernet (AES-128-CBC with HMAC-SHA256)."""

    def __init__(self, encryption_key):
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()
        self.cipher = Fernet(encryption_key)

    def encrypt(self, data):
        """Encrypts a plaintext string into a URL-safe base64 encrypted token."""
        if data is None or data == '':
            return None
        if isinstance(data, str):
            data = data.encode('utf-8')
        encrypted_data = self.cipher.encrypt(data)
        return encrypted_data.decode('utf-8')

    def decrypt(self, encrypted_data):
        """Decrypts a base64 ciphertext token back into plaintext string."""
        if encrypted_data is None or encrypted_data == '':
            return None
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
