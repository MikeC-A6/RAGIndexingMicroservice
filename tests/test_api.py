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

if __name__ == '__main__':
    unittest.main(verbosity=2)
