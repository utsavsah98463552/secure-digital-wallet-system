import unittest
import os
import sys
import bcrypt
from cryptography.fernet import Fernet, InvalidToken
from services.encryption_service import EncryptionService

class TestEncryptionService(unittest.TestCase):
    """Unit tests for Fernet symmetric encryption and bcrypt password hashing."""

    def setUp(self):
        self.encryption_key = Fernet.generate_key()
        self.encryption_service = EncryptionService(self.encryption_key)

    def test_encrypt_decrypt(self):
        """Verify encryption produces ciphertext and decrypt restores plaintext."""
        original_data = 'Confidential memo: Invoice #4092 payment settlement'

        encrypted = self.encryption_service.encrypt(original_data)
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(original_data, encrypted)

        decrypted = self.encryption_service.decrypt(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_encrypt_empty_string(self):
        """Verify empty string returns None."""
        encrypted = self.encryption_service.encrypt('')
        self.assertIsNone(encrypted)

    def test_encrypt_none(self):
        """Verify None input returns None."""
        encrypted = self.encryption_service.encrypt(None)
        self.assertIsNone(encrypted)

    def test_decrypt_none(self):
        """Verify decrypting None returns None."""
        decrypted = self.encryption_service.decrypt(None)
        self.assertIsNone(decrypted)

    def test_encrypt_unicode_and_emojis(self):
        """Verify encryption preserves Unicode characters and emojis."""
        original_data = 'Digital Payment 💸 for Momo Lunch 🥟 🇳🇵'

        encrypted = self.encryption_service.encrypt(original_data)
        decrypted = self.encryption_service.decrypt(encrypted)

        self.assertEqual(original_data, decrypted)

    def test_tampered_token_detection(self):
        """Verify HMAC integrity check fails if ciphertext is tampered with."""
        original_data = 'Secret payload'
        encrypted = self.encryption_service.encrypt(original_data)

        # Tamper with the ciphertext (swap a middle character)
        tampered = encrypted[:-5] + ('A' if encrypted[-5] != 'A' else 'B') + encrypted[-4:]
        with self.assertRaises(InvalidToken):
            self.encryption_service.cipher.decrypt(tampered.encode('utf-8'))

    def test_bcrypt_password_hashing(self):
        """Verify bcrypt generates unique salts and verifies plaintext passwords correctly."""
        password = "SecureSuperSecretPassword123!"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        self.assertNotEqual(password, hashed.decode('utf-8'))
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))
        self.assertFalse(bcrypt.checkpw("WrongPassword!".encode('utf-8'), hashed))

if __name__ == '__main__':
    unittest.main()
