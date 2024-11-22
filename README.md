# Indexing Microservice for RAG Pipeline

This microservice is responsible for processing raw documents and generating structured output for the RAG (Retrieval-Augmented Generation) pipeline. It handles document preprocessing, applies various indexing strategies, and formats output for downstream embedding services.

## Architecture Overview

The service is organized into four main components:

1. API Gateway
   - Handles incoming requests
   - Manages request validation and routing
   - Exposes endpoints for document ingestion and strategy listing

2. Indexing Strategy Manager
   - Manages different indexing strategies
   - Supports extensible indexing modules
   - Currently supports SimpleDirectoryReader and JSON indexing

3. Preprocessing Module
   - Handles document cleaning and text extraction
   - Supports various document formats (Text, PDF)
   - Manages document chunking

4. Output Formatter
   - Standardizes output format
   - Ensures compatibility with the Embedding Service

## Project Structure

```
├── src/                    # Source code directory
│   ├── api/               # API Gateway implementation
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoint definitions
│   ├── indexing/          # Indexing strategy implementations
│   │   ├── strategies/    # Individual indexing strategies
│   │   │   ├── simple_directory_reader.py
│   │   │   └── json_indexer.py
│   │   ├── base.py       # Base indexing interface
│   │   └── strategy_manager.py
│   ├── output/           # Output formatting
│   │   └── formatter.py  # Standardized output formatter
│   ├── preprocessing/    # Document preprocessing
│   │   ├── extractors/   # Text extraction implementations
│   │   │   ├── text_extractor.py
│   │   │   └── pdf_extractor.py
│   │   └── processor.py  # Main preprocessing logic
│   ├── utils/           # Utility functions
│   │   └── validators.py # Request validation
│   ├── config.py        # Application configuration
│   └── main.py         # Application entry point
├── tests/              # Test suite
│   ├── test_api.py     # API endpoint tests
│   ├── test_indexing.py # Indexing strategy tests
│   ├── test_preprocessing.py # Preprocessing tests
│   └── test_output.py  # Output formatting tests
```

## Module Descriptions

### API Gateway (`src/api/`)
- `routes.py`: Implements REST endpoints for document ingestion and strategy listing
- Handles request validation and error responses
- Routes requests to appropriate processing components

### Indexing (`src/indexing/`)
- `base.py`: Defines the base interface for indexing strategies
- `strategy_manager.py`: Manages and coordinates different indexing strategies
- **Strategies**:
  - `simple_directory_reader.py`: Directory-based document processing using LlamaIndex integration
     - Recursively processes all files in a directory
     - Supports automatic file type detection
     - Maintains file metadata and structure
     - Integrates with LlamaIndex's SimpleDirectoryReader
  - `json_indexer.py`: Specialized JSON document processing with path tracking

### Preprocessing (`src/preprocessing/`)
- `processor.py`: Coordinates document preprocessing workflow
- **Extractors**:
  - `text_extractor.py`: Plain text document handling
  - `pdf_extractor.py`: PDF document text extraction

### Output (`src/output/`)
- `formatter.py`: Standardizes processed data for embedding service consumption
- Ensures consistent metadata structure

### Utils (`src/utils/`)
- `validators.py`: Input validation utilities for requests and files
- Supports file type and size validation

## Component Relationships

1. **Request Flow**:
   ```
   Client Request → API Gateway → Preprocessing → Indexing → Output Formatter → Response
   ```

2. **Strategy Selection**:
   ```
   API Gateway → Strategy Manager → Specific Indexing Strategy
   ```

3. **Document Processing**:
   ```
   Preprocessing Module → Text/PDF Extractor → Indexing Strategy → Output Formatter
   ```

## Test Organization

The test suite is organized to mirror the main package structure:

### Unit Tests
- `test_api.py`: API endpoint functionality and error handling
- `test_indexing.py`: Individual indexing strategy implementations
- `test_preprocessing.py`: Document preprocessing and extraction
- `test_output.py`: Output formatting and standardization

### Test Coverage
- Each component has dedicated test cases
- Tests verify both success and error scenarios
- Integration points between components are tested

## Configuration

The service configuration (`config.py`) includes:
- Maximum file size limits
- Allowed file extensions
- Default preprocessing settings
- Environment-specific configurations

## Usage Examples

### Document Ingestion Examples

#### 1. Single Document Processing
```python
POST /api/ingest
{
    "client_id": "client123",
    "documents": [{
        "content": "document content",
        "type": "txt",
        "metadata": {"source": "example.txt"}
    }],
    "indexing_strategy": "json_index"
}
```

#### 2. Directory Processing with SimpleDirectoryReader
```python
POST /api/ingest
{
    "client_id": "client123",
    "documents": [{
        "content": "",
        "type": "directory",
        "metadata": {
            "directory_path": "/path/to/documents",
            "source": "document_collection"
        }
    }],
    "indexing_strategy": "simple_directory"
}
```

The SimpleDirectoryReader strategy provides:
- Recursive directory traversal
- Automatic file type detection
- Metadata preservation
- File path tracking
- Timestamp generation
- Chunk indexing

Response format for directory processing:
```python
[
    {
        "content": "Extracted text content from file",
        "metadata": {
            "source": "/path/to/documents/file1.txt",
            "chunk_index": 0,
            "timestamp": "2024-11-22T14:30:00",
            "strategy": "simple_directory",
            "file_type": ".txt",
            "original_metadata": {
                "file_path": "/path/to/documents/file1.txt",
                # Additional LlamaIndex metadata
            }
        }
    }
    # Additional documents...
]
```

### List Available Strategies
```python
GET /api/list-strategies
Response: ["simple_directory", "json_index"]
```

### SimpleDirectoryReader Configuration
The SimpleDirectoryReader strategy uses LlamaIndex's SimpleDirectoryReader with the following default settings:
- `recursive=True`: Processes subdirectories recursively
- `filename_as_id=True`: Uses filenames as document identifiers
- Supports all common document formats (txt, pdf, etc.)
- Preserves file hierarchy in metadata

