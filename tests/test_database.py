import unittest
import sqlite3
import tempfile
import os
from database import Database

class TestDatabaseLayer(unittest.TestCase):
    """Unit tests for SQLite persistence, schema initialization, and transactional safety."""

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp()
        self.db = Database(self.temp_db_path)

    def tearDown(self):
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_tables_created(self):
        """Verify that users, wallets, and transactions tables are created on initialization."""
        rows = self.db.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'wallets', 'transactions')"
        )
        table_names = [row['name'] for row in rows]
        self.assertIn('users', table_names)
        self.assertIn('wallets', table_names)
        self.assertIn('transactions', table_names)

    def test_insert_and_query_user(self):
        """Verify inserting a user and executing parameterized SELECT."""
        user_id = self.db.execute_insert(
            "INSERT INTO users (username, email, password_hash, otp_secret) VALUES (?, ?, ?, ?)",
            ("alice", "alice@example.com", "hashed_pw", "secret_key")
        )
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)

        rows = self.db.execute_query("SELECT * FROM users WHERE username = ?", ("alice",))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['email'], "alice@example.com")

    def test_unique_constraint(self):
        """Verify unique constraint on username."""
        self.db.execute_insert(
            "INSERT INTO users (username, email, password_hash, otp_secret) VALUES (?, ?, ?, ?)",
            ("bob", "bob@example.com", "hash", "secret")
        )
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute_insert(
                "INSERT INTO users (username, email, password_hash, otp_secret) VALUES (?, ?, ?, ?)",
                ("bob", "other@example.com", "hash2", "secret2")
            )

    def test_transaction_rollback_on_error(self):
        """Verify that atomic context rolls back all operations if an exception occurs."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, otp_secret) VALUES (?, ?, ?, ?)",
                    ("charlie", "charlie@example.com", "hash", "secret")
                )
                # Intentionally trigger an error
                raise RuntimeError("Simulated transaction failure")
        except RuntimeError:
            pass

        rows = self.db.execute_query("SELECT * FROM users WHERE username = ?", ("charlie",))
        self.assertEqual(len(rows), 0, "Changes should have been rolled back!")

if __name__ == '__main__':
    unittest.main()
