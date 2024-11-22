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
