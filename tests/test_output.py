import unittest
from datetime import datetime
from src.output.formatter import OutputFormatter

class TestOutput(unittest.TestCase):
    def setUp(self):
        self.formatter = OutputFormatter()
        
    def test_output_formatting_with_validation(self):
        """Test output formatting with metadata validation."""
        test_data = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.txt',
                'chunk_index': 1,
                'timestamp': '2024-01-01',
                'document_type': 'text',
                'version': '1.0.0'
            }
        }]
        
        formatted = self.formatter.format(test_data)
        
        self.assertTrue(len(formatted) > 0)
        self.assertTrue('text' in formatted[0])
        self.assertTrue('metadata' in formatted[0])
        self.assertEqual(formatted[0]['text'], 'Test content')
        self.assertTrue('processed_at' in formatted[0]['metadata'])
        self.assertTrue('content_length' in formatted[0]['metadata'])
        
    def test_versioning_support(self):
        """Test version increment functionality."""
        test_data = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.txt',
                'timestamp': '2024-01-01',
                'document_type': 'text',
                'version': '1.0.0'
            }
        }]
        
        formatted = self.formatter.format(test_data, version_increment=True)
        self.assertEqual(formatted[0]['metadata']['version'], '1.0.1')
        
    def test_metadata_validation(self):
        """Test metadata validation and enrichment."""
        test_data = [{
            'content': 'Test content',
            'metadata': {
                'source': 'test.txt'
            }
        }]
        
        formatted = self.formatter.format(test_data)
        metadata = formatted[0]['metadata']
        
        self.assertTrue('version' in metadata)
        self.assertTrue('timestamp' in metadata)
        self.assertTrue('document_type' in metadata)
        self.assertEqual(metadata['document_type'], 'text_document')
        
    def test_document_type_detection(self):
        """Test automatic document type detection from file extensions."""
        test_cases = [
            ('document.pdf', 'pdf_document'),
            ('notes.txt', 'text_document'),
            ('data.json', 'json_document'),
            ('doc.docx', 'word_document'),
            ('page.html', 'html_document'),
            ('unknown.xyz', 'unknown_document')
        ]
        
        for filename, expected_type in test_cases:
            test_data = [{
                'content': 'Test content',
                'metadata': {
                    'source': filename
                }
            }]
            
            formatted = self.formatter.format(test_data)
            metadata = formatted[0]['metadata']
            self.assertEqual(
                metadata['document_type'], 
                expected_type,
                f"Failed to detect correct document type for {filename}"
            )
        
    def test_empty_data_handling(self):
        """Test formatting of empty data."""
        formatted = self.formatter.format([])
        self.assertEqual(len(formatted), 0)

if __name__ == '__main__':
    unittest.main()
