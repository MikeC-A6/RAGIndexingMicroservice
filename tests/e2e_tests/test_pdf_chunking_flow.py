import unittest
import os
import json
from src.main import create_app

class TestPDFChunkingFlow(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_docs_dir = "test_docs"

    def test_pdf_sentence_chunking_end_to_end(self):
        """Test end-to-end PDF ingestion with sentence chunking strategy."""
        test_pdf_path = os.path.join(self.test_docs_dir, "Test_PDF1.pdf")

        if not os.path.exists(test_pdf_path):
            self.skipTest(f"Test_PDF1.pdf not found at {test_pdf_path}")

        test_data = {
            "documents": [{
                "metadata": {
                    "directory_path": self.test_docs_dir,
                    "file_pattern": "*.pdf"
                }
            }],
            "indexing_strategy": "sentence_chunker",
            "chunk_params": {
                "max_sentences_per_chunk": 3,
                "min_sentence_length": 10,
                "overlap_sentences": 1
            }
        }

        # Print test configuration
        print("\nTest Configuration:")
        print(f"PDF Path: {test_pdf_path}")
        print(f"Strategy: {test_data['indexing_strategy']}")
        print(f"Chunk Parameters: {test_data['chunk_params']}")

        # Changed endpoint to include /api prefix
        response = self.client.post('/api/ingest', 
                                  json=test_data,
                                  content_type='application/json')

        print("\nResponse Status:", response.status_code)

        # Add error handling
        if response.status_code != 200:
            print("Error Response:", response.get_json())
            self.fail(f"Request failed with status {response.status_code}")

        result = response.get_json()

if __name__ == '__main__':
    unittest.main()