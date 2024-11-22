import os
import sys
from pathlib import Path
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.handlers.RotatingFileHandler(
            'app.log',
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3
        )
    ]
)

# Set external library logging levels
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('gunicorn').setLevel(logging.INFO)

# Add the project root directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

try:
    from src.main import create_app
    app = create_app()
    logging.info("Application created successfully")
except Exception as e:
    logging.error(f"Failed to create application: {e}")
    raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
