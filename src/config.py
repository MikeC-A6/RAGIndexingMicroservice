class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = 'development-key'  # Change in production
    
    # Service settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'json'}
    
    # Preprocessing settings
    DEFAULT_CHUNK_SIZE = 1000
    ENABLE_OCR = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # Production security settings
    STRICT_TRANSPORT_SECURITY = True
    CONTENT_SECURITY_POLICY = True
    # Ensure proper host binding
    HOST = '0.0.0.0'
    PORT = 5000
    # Production security features
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
