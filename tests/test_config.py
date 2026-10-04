import unittest
from config import config, DevelopmentConfig, ProductionConfig, TestingConfig

class TestConfiguration(unittest.TestCase):
    """Test environment configurations and security defaults."""

    def test_development_config(self):
        cfg = DevelopmentConfig()
        self.assertTrue(cfg.DEBUG)
        self.assertFalse(cfg.SESSION_COOKIE_SECURE)
        self.assertTrue(cfg.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(cfg.PERMANENT_SESSION_LIFETIME, 1800)

    def test_production_config(self):
        cfg = ProductionConfig()
        self.assertFalse(cfg.DEBUG)
        self.assertTrue(cfg.SESSION_COOKIE_SECURE)
        self.assertTrue(cfg.SESSION_COOKIE_HTTPONLY)

    def test_testing_config(self):
        cfg = TestingConfig()
        self.assertTrue(cfg.TESTING)
        self.assertEqual(cfg.DATABASE_PATH, ':memory:')

    def test_keys_generated_or_present(self):
        cfg = DevelopmentConfig()
        self.assertIsNotNone(cfg.SECRET_KEY)
        self.assertIsNotNone(cfg.ENCRYPTION_KEY)
        self.assertTrue(len(cfg.SECRET_KEY) > 0)

if __name__ == '__main__':
    unittest.main()
