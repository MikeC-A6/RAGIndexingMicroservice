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

    def tearDown(self):
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir)

    def test_ingest_endpoint(self):
        """Test document ingestion endpoint."""
        # Test data
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

        # Test successful request
        response = self.client.post(
            '/ingest',
            json=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Test invalid request
        invalid_data = {"documents": []}
        response = self.client.post(
            '/ingest',
            json=invalid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_ingest_with_directory(self):
        """Test document ingestion endpoint with directory strategy."""
        data = {
            "client_id": "test_client",
            "documents": [
                {
                    "content": "",  # Content is empty as we're using directory
                    "type": "directory",
                    "metadata": {
                        "directory_path": self.test_dir,
                        "source": "test_directory"
                    }
                }
            ],
            "indexing_strategy": "simple_directory"
        }

        response = self.client.post(
            '/ingest',
            json=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        result = response.get_json()

        # Verify the response contains indexed documents
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) > 0)

        # Verify metadata in response
        for doc in result:
            self.assertIn('metadata', doc)
            self.assertEqual(doc['metadata']['strategy'], 'simple_directory')
            self.assertTrue('file_path' in doc['metadata'])
            self.assertTrue('timestamp' in doc['metadata'])

    def test_list_strategies_endpoint(self):
        """Test listing available strategies endpoint."""
        response = self.client.get('/list-strategies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('simple_directory', data)
        self.assertIn('json_index', data)

if __name__ == '__main__':
    unittest.main()
