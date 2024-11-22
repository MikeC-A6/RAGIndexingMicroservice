import unittest
from src.output.formatter import OutputFormatter

class TestOutput(unittest.TestCase):
    def setUp(self):
        self.formatter = OutputFormatter()
        
    def test_output_formatting(self):
        """Test output formatting for embedding service."""
        test_data = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.txt',
                'chunk_index': 1,
                'timestamp': '2024-01-01'
            }
        }]
        
        formatted = self.formatter.format(test_data)
        
        self.assertTrue(len(formatted) > 0)
        self.assertTrue('text' in formatted[0])
        self.assertTrue('metadata' in formatted[0])
        self.assertEqual(formatted[0]['text'], 'Test content')
        self.assertEqual(formatted[0]['metadata']['chunk_index'], 1)
        
    def test_empty_data_handling(self):
        """Test formatting of empty data."""
        formatted = self.formatter.format([])
        self.assertEqual(len(formatted), 0)

if __name__ == '__main__':
    unittest.main()
