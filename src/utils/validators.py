from typing import Dict, Any
import os

def validate_request_data(data: Dict[str, Any]) -> bool:
    """Validate incoming request data."""
    required_fields = ['client_id', 'documents', 'indexing_strategy']
    return all(field in data for field in required_fields)

def validate_file_type(filename: str, allowed_extensions: set) -> bool:
    """Check if file type is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Check if file size is within limits."""
    return file_size <= max_size
