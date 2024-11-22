import unittest
from src.indexing.strategies import SimpleDirectoryReader, JSONIndexer

class TestIndexing(unittest.TestCase):
    def setUp(self):
        self.simple_reader = SimpleDirectoryReader()
        self.json_indexer = JSONIndexer()
        
    def test_simple_directory_reader(self):
        """Test SimpleDirectoryReader indexing."""
        test_docs = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.txt',
                'timestamp': '2024-01-01'
            }
        }]
        
        result = self.simple_reader.index(test_docs)
        
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['content'], 'Test content')
        self.assertEqual(result[0]['metadata']['strategy'], 'simple_directory')
        
    def test_json_indexer(self):
        """Test JSONIndexer indexing."""
        test_docs = [{
            'content': '{"key": "value", "nested": {"inner": "data"}}',
            'metadata': {
                'source': 'test.json',
                'timestamp': '2024-01-01'
            }
        }]
        
        result = self.json_indexer.index(test_docs)
        
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['metadata']['strategy'], 'json_index')
        self.assertTrue(any(chunk['metadata']['json_path'] == 'nested.inner' 
                          for chunk in result))
    
    def test_simple_directory_reader_with_file_pattern(self):
        """Test SimpleDirectoryReader with PDF file pattern."""
        test_docs = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.pdf',
                'timestamp': '2024-01-01',
                'directory_path': './test_docs',  # Make sure this directory exists
                'file_pattern': '*.pdf'
            }
        }]

        result = self.simple_reader.index(test_docs)

        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0]['metadata']['source'].endswith('.pdf'))

if __name__ == '__main__':
    unittest.main()
