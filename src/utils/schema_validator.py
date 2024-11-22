from typing import Dict, Any, List, Optional
from datetime import datetime

class SchemaValidator:
    """Validates document metadata against predefined schemas."""
    
    REQUIRED_METADATA_FIELDS = {
        'source': str,
        'timestamp': str,
        'version': str,
        'document_type': str
    }
    
    @classmethod
    def validate_metadata(cls, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enrich metadata with required fields."""
        validated_metadata = metadata.copy()
        
        # Add version if not present
        if 'version' not in validated_metadata:
            validated_metadata['version'] = '1.0.0'
            
        # Add timestamp if not present
        if 'timestamp' not in validated_metadata:
            validated_metadata['timestamp'] = datetime.now().isoformat()
            
        # Add document_type if not present
        if 'document_type' not in validated_metadata:
            validated_metadata['document_type'] = 'unknown'
            
        # Validate required fields
        missing_fields = []
        invalid_types = []
        
        for field, expected_type in cls.REQUIRED_METADATA_FIELDS.items():
            if field not in validated_metadata:
                missing_fields.append(field)
            elif not isinstance(validated_metadata[field], expected_type):
                invalid_types.append(f"{field} (expected {expected_type.__name__})")
                
        if missing_fields or invalid_types:
            error_msg = []
            if missing_fields:
                error_msg.append(f"Missing required fields: {', '.join(missing_fields)}")
            if invalid_types:
                error_msg.append(f"Invalid field types: {', '.join(invalid_types)}")
            raise ValueError(". ".join(error_msg))
            
        return validated_metadata

    @classmethod
    def increment_version(cls, current_version: str) -> str:
        """Increment document version following semver pattern."""
        try:
            major, minor, patch = map(int, current_version.split('.'))
            return f"{major}.{minor}.{patch + 1}"
        except (ValueError, AttributeError):
            return "1.0.0"  # Default to initial version if invalid
