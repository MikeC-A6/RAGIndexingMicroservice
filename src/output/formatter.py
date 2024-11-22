from typing import List, Dict, Any, Optional
from src.utils.schema_validator import SchemaValidator
from datetime import datetime

class OutputFormatter:
    """Formats indexed data for the Embedding Service with enhanced metadata support."""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        
    def format(self, indexed_data: List[Dict[str, Any]], version_increment: bool = False) -> List[Dict[str, Any]]:
        """
        Format indexed data into standardized output with validated metadata.
        
        Args:
            indexed_data: List of indexed documents with content and metadata
            version_increment: If True, increment version number of documents
            
        Returns:
            List of formatted documents with validated metadata
        """
        formatted_output = []

        for item in indexed_data:
            content = item.get('content', '')
            metadata = item.get('metadata', {})
            
            # Handle versioning
            if version_increment and 'version' in metadata:
                metadata['version'] = self.schema_validator.increment_version(metadata['version'])
            
            # Validate and enrich metadata
            try:
                validated_metadata = self.schema_validator.validate_metadata(metadata)
            except ValueError as e:
                print(f"Warning: Metadata validation failed: {str(e)}")
                validated_metadata = metadata
            
            # Add processing metadata
            validated_metadata.update({
                'processed_at': datetime.now().isoformat(),
                'content_length': len(content),
                'has_validation_errors': False
            })
            
            formatted_chunk = {
                'text': content,
                'metadata': validated_metadata
            }
            formatted_output.append(formatted_chunk)

        return formatted_output
