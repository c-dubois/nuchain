from .settings import * # noqa: F405

# Override database to use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# Disable migrations during tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None
    
MIGRATION_MODULES = DisableMigrations()

# Fast password hashing for tests
# This is not secure and should only be used in a testing environment
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable security features for testing
DEBUG = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Blockchain settings for testing (mocked)
BASE_SEPOLIA_RPC_URL = 'https://sepolia.base.org'
NUC_CONTRACT_ADDRESS = '0x7a8ed93c1eA030eC8F283e93Ff1BB008e57D4791'
ADMIN_PRIVATE_KEY = '0x' + '1' * 64  # Fake key for testing