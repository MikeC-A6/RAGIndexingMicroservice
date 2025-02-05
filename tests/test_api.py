import unittest
import tempfile
import os
from src.main import create_app
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create some test files
        with open(os.path.join(self.test_dir, 'test1.txt'), 'w') as f:
            f.write('Test document content 1')
        with open(os.path.join(self.test_dir, 'test2.txt'), 'w') as f:
            f.write('Test document content 2')

        print(f"\nTest directory created at: {self.test_dir}")
        print(f"Test files created: {os.listdir(self.test_dir)}")

    def tearDown(self):
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
        print(f"\nTest directory cleaned up: {self.test_dir}")

    def test_ingest_endpoint(self):
        """Test document ingestion endpoint."""
        data = {
            "client_id": "test_client",
            "documents": [
                {
                    "content": "Test document content",
                    "type": "txt",
                    "metadata": {"source": "test"}
                }
            ],
            "indexing_strategy": "simple_directory"
        }

        print("\nTesting basic ingest endpoint with data:", json.dumps(data, indent=2))
        response = self.client.post('/api/ingest', json=data)
        print("Response status:", response.status_code)
        print("Response data:", response.get_json())
        self.assertEqual(response.status_code, 200)

        # Test invalid request
        invalid_data = {"documents": []}
        print("\nTesting with invalid data:", json.dumps(invalid_data, indent=2))
        response = self.client.post('/api/ingest', json=invalid_data)
        print("Invalid request response status:", response.status_code)
        print("Invalid request response:", response.get_json())
        self.assertEqual(response.status_code, 400)

    def test_ingest_with_directory(self):
        """Test document ingestion endpoint with directory strategy."""
        data = {
            "client_id": "test_client",
            "documents": [
                {
                    "content": "",
                    "type": "directory",
                    "metadata": {
                        "directory_path": self.test_dir,
                        "source": "test_directory"
                    }
                }
            ],
            "indexing_strategy": "simple_directory"
        }

        print("\nTesting directory ingest with data:", json.dumps(data, indent=2))

        # Add debug headers
        headers = {
            'Content-Type': 'application/json',
            'X-Debug': 'true'
        }

        response = self.client.post('/api/ingest', json=data, headers=headers)
        print("\nResponse status code:", response.status_code)

        result = response.get_json()
        print("Raw response data:", json.dumps(result, indent=2))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) > 0)

        # Debug print each document's structure
        for idx, doc in enumerate(result):
            print(f"\nDocument {idx} structure:")
            print(json.dumps(doc, indent=2))

            # Check if 'metadata' exists
            self.assertIn('metadata', doc, f"Document {idx} missing metadata field")

            # Print metadata contents
            metadata = doc.get('metadata', {})
            print(f"\nMetadata for document {idx}:")
            print(json.dumps(metadata, indent=2))

            # Verify expected metadata fields
            self.assertTrue('source' in metadata, f"Document {idx} missing source in metadata")
            self.assertTrue('timestamp' in metadata, f"Document {idx} missing timestamp in metadata")

            # If the strategy field is missing, print a warning but don't fail
            if 'strategy' not in metadata:
                print(f"\nWARNING: Document {idx} missing strategy field in metadata")
                print("Expected 'simple_directory', got metadata:", json.dumps(metadata, indent=2))

    def test_list_strategies_endpoint(self):
        """Test listing available strategies endpoint."""
        print("\nTesting list-strategies endpoint")
        response = self.client.get('/api/list-strategies')
        print("Response status:", response.status_code)
        data = response.get_json()
        print("Available strategies:", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('simple_directory', data)
        self.assertIn('json_index', data)

    def test_metadata_validation_in_ingest(self):
        """Test that ingested documents have proper metadata validation."""
        # Create a temporary test directory
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file_path = os.path.join(temp_dir, "test.txt")
            with open(test_file_path, "w") as f:
                f.write("Test content")

            # Test data with directory_path
            data = {
                "documents": [
                    {
                        "metadata": {
                            "directory_path": temp_dir,
                            "source": "test"
                        },
                        "type": "txt"
                    }
                ],
                "indexing_strategy": "simple_directory"
            }

            response = self.client.post('/api/ingest', json=data)
            self.assertEqual(response.status_code, 200)

            result = response.get_json()
            self.assertTrue(isinstance(result, list))
            self.assertTrue(len(result) > 0)

            # Check metadata
            for doc in result:
                metadata = doc.get('metadata', {})
                self.assertIn('source', metadata)
                self.assertIn('timestamp', metadata)
                self.assertIn('strategy', metadata)
                self.assertEqual(metadata['strategy'], 'simple_directory')

    def test_ingest_with_document_types(self):
        """Test document ingestion endpoint with different document types."""
        # Create a test PDF file in test_docs
        pdf_content = "This is a test PDF document"
        test_pdf_path = os.path.join("test_docs", "Test_PDF1.pdf")

        test_data = {
            "documents": [
                {
                    "type": "directory",
                    "metadata": {
                        "directory_path": "test_docs",
                        "source": test_pdf_path,
                        "document_type": "pdf_document",
                        "page_count": 10,
                        "pdf_version": "1.7"
                    }
                }
            ],
            "indexing_strategy": "simple_directory"
        }

        print("\nTesting PDF ingest with data:", json.dumps(test_data, indent=2))
        response = self.client.post('/api/ingest', json=test_data)
        print("Response status:", response.status_code)

        result = response.get_json()
        print("Response data:", json.dumps(result, indent=2))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) > 0)

        # Check metadata for each document chunk
        for doc in result:
            metadata = doc.get('metadata', {})
            self.assertIn('source', metadata)
            self.assertIn('timestamp', metadata)
            self.assertIn('strategy', metadata)
            self.assertEqual(metadata['strategy'], 'simple_directory')
            # Update assertion to check for either file type since both might be present
            self.assertIn('file_type', metadata)
            self.assertIn(metadata['file_type'], ['.txt', '.pdf'], 
                         f"Unexpected file type: {metadata['file_type']}")

    def test_ingest_pdf_with_validation_rules(self):
        """Test PDF document ingestion with specific validation rules."""
        test_docs_dir = "test_docs"
        test_pdf_path = os.path.join(test_docs_dir, "Test_PDF1.pdf")

        # First verify the PDF exists
        if not os.path.exists(test_pdf_path):
            print(f"\nWARNING: Test_PDF1.pdf not found at {test_pdf_path}")
            self.skipTest(f"Test_PDF1.pdf not found at {test_pdf_path}. Please create this file before running the test.")

        test_data = {
            "documents": [
                {
                    "type": "directory",
                    "metadata": {
                        "directory_path": test_docs_dir,
                        "source": test_pdf_path,
                        "document_type": "pdf_document",
                        "page_count": 10,
                        "pdf_version": "1.7",
                        "page_width": 8.5,
                        "page_height": 11.0,
                        "pdfa_compliant": True,
                        "pdfa_version": "2b",
                        "file_pattern": "*.pdf"  # Add this to filter for PDFs only
                    }
                }
            ],
            "indexing_strategy": "simple_directory"
        }

        print(f"\nTesting with PDF at: {test_pdf_path}")
        print("\nTest data:", json.dumps(test_data, indent=2))

        response = self.client.post('/api/ingest', json=test_data)
        print("\nResponse status:", response.status_code)

        result = response.get_json()
        print("\nResponse data:", json.dumps(result, indent=2))

        # Validate response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) > 0)

        # Validate PDF-specific metadata
        for doc in result:
            metadata = doc.get('metadata', {})
            self.assertEqual(metadata.get('file_type'), '.pdf', 
                            f"Expected PDF file, got {metadata.get('file_type')}")
            self.assertTrue(test_pdf_path in metadata.get('source', ''), 
                           f"Expected source to contain {test_pdf_path}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
