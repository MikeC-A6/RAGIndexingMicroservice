from typing import List, Dict, Any
from datetime import datetime
from src.utils.schema_validator import SchemaValidator

class OutputFormatter:
    """Formats indexed data for the Embedding Service with enhanced metadata support."""

    FILE_EXTENSION_TO_DOCTYPE = {
        '.pdf': 'pdf_document',
        '.txt': 'text_document',
        '.json': 'json_document',
        '.docx': 'word_document',
        '.html': 'html_document'
    }

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

            # Determine document type from source file extension
            source = metadata.get('source', '')
            extension = source[source.rfind('.'):].lower() if '.' in source else ''
            doc_type = self.FILE_EXTENSION_TO_DOCTYPE.get(extension, 'unknown_document')
            metadata['document_type'] = doc_type

            # Add default metadata based on document type
            if doc_type == 'text_document' and 'encoding' not in metadata:
                metadata['encoding'] = 'utf-8'
            elif doc_type == 'pdf_document':
                if 'pdf_version' not in metadata:
                    metadata['pdf_version'] = '1.7'
                if 'page_count' not in metadata:
                    metadata['page_count'] = 0
            elif doc_type == 'json_document' and 'schema_version' not in metadata:
                metadata['schema_version'] = '1.0'

            # Handle versioning
            if version_increment and 'version' in metadata:
                metadata['version'] = self.schema_validator.increment_version(metadata['version'])

            # Validate and enrich metadata
            try:
                validated_metadata = self.schema_validator.validate_metadata(metadata)
            except ValueError as e:
                print(f"Warning: Metadata validation failed: {str(e)}")
                validated_metadata = metadata
                validated_metadata['has_validation_errors'] = True

            # Add processing metadata
            validated_metadata.update({
                'processed_at': datetime.now().isoformat(),
                'content_length': len(content),
                'has_validation_errors': validated_metadata.get('has_validation_errors', False)
            })

            formatted_chunk = {
                'text': content,
                'metadata': validated_metadata
            }
            formatted_output.append(formatted_chunk)

        return formatted_output
