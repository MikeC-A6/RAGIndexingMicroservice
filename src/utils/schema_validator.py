from typing import Dict, Any, List, Optional
from datetime import datetime
import os

class SchemaValidator:
    """Validates document metadata against predefined schemas with custom rules per document type."""

    REQUIRED_METADATA_FIELDS = {
        'source': str,
        'timestamp': str,
        'version': str,
        'document_type': str
    }

    FILE_EXTENSION_TO_DOCTYPE = {
        '.txt': 'text_document',
        '.pdf': 'pdf_document',
        '.doc': 'word_document',
        '.docx': 'word_document',
        '.md': 'markdown_document',
        '.json': 'json_document',
        '.xml': 'xml_document',
        '.csv': 'csv_document',
        '.html': 'html_document',
        '.htm': 'html_document'
    }

    # Custom validation rules per document type
    DOCUMENT_TYPE_RULES = {
        'pdf_document': {
            'required_fields': {'page_count': int, 'pdf_version': str},
            'optional_fields': {'author': str, 'title': str},
            'validation_functions': []
        },
        'text_document': {
            'required_fields': {'encoding': str},
            'optional_fields': {'line_count': int},
            'validation_functions': []
        },
        'json_document': {
            'required_fields': {'schema_version': str},
            'optional_fields': {'root_keys': list},
            'validation_functions': []
        },
        'word_document': {
            'required_fields': {'word_version': str},
            'optional_fields': {'author': str, 'title': str, 'last_modified': str},
            'validation_functions': []
        },
        'html_document': {
            'required_fields': {'html_version': str},
            'optional_fields': {'meta_tags': dict, 'encoding': str},
            'validation_functions': []
        }
    }

    @classmethod
    def validate_metadata(cls, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enrich metadata with required fields and document-specific rules."""
        validated_metadata = metadata.copy()

        # Add common required fields if not present
        if 'version' not in validated_metadata:
            validated_metadata['version'] = '1.0.0'
        if 'timestamp' not in validated_metadata:
            validated_metadata['timestamp'] = datetime.now().isoformat()

        # Determine document type from source file extension
        source = validated_metadata.get('source', '')
        if source:
            file_ext = os.path.splitext(source)[1].lower()
            validated_metadata['document_type'] = cls.FILE_EXTENSION_TO_DOCTYPE.get(
                file_ext, 'unknown_document'
            )
        elif 'document_type' not in validated_metadata:
            validated_metadata['document_type'] = 'unknown_document'

        # Validate common required fields
        missing_fields = []
        invalid_types = []

        for field, expected_type in cls.REQUIRED_METADATA_FIELDS.items():
            if field not in validated_metadata:
                missing_fields.append(field)
            elif not isinstance(validated_metadata[field], expected_type):
                invalid_types.append(f"{field} (expected {expected_type.__name__})")

        # Apply document type specific validation rules
        doc_type = validated_metadata.get('document_type')
        if doc_type in cls.DOCUMENT_TYPE_RULES:
            type_rules = cls.DOCUMENT_TYPE_RULES[doc_type]
            
            # Validate required fields for document type
            for field, expected_type in type_rules['required_fields'].items():
                if field not in validated_metadata:
                    missing_fields.append(f"{doc_type}.{field}")
                elif not isinstance(validated_metadata[field], expected_type):
                    invalid_types.append(f"{field} (expected {expected_type.__name__})")

            # Add default values for optional fields if not present
            for field, field_type in type_rules['optional_fields'].items():
                if field not in validated_metadata:
                    if field_type == str:
                        validated_metadata[field] = ''
                    elif field_type == int:
                        validated_metadata[field] = 0
                    elif field_type == list:
                        validated_metadata[field] = []
                    elif field_type == dict:
                        validated_metadata[field] = {}

            # Apply custom validation functions if any
            for validation_func in type_rules.get('validation_functions', []):
                try:
                    validation_func(validated_metadata)
                except Exception as e:
                    invalid_types.append(f"Custom validation failed: {str(e)}")

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
