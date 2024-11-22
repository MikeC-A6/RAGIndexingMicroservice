import unittest
from src.main import create_app
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
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
        
    def test_list_strategies_endpoint(self):
        """Test listing available strategies endpoint."""
        response = self.client.get('/list-strategies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('simple_directory', data)
        self.assertIn('json_index', data)

if __name__ == '__main__':
    unittest.main()
