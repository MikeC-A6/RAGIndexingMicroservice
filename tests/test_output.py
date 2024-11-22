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
        
    def test_document_specific_validation_rules(self):
        """Test validation rules specific to different document types."""
        # Test PDF document validation
        pdf_data = [{
            'content': 'PDF content',
            'metadata': {
                'source': 'test.pdf',
                'timestamp': '2024-01-01',
                'page_count': 10,
                'pdf_version': '1.7',
                'page_width': 8.5,
                'page_height': 11.0,
                'pdfa_compliant': True,
                'pdfa_version': '2b'
            }
        }]
        
        formatted = self.formatter.format(pdf_data)
        metadata = formatted[0]['metadata']
        self.assertEqual(metadata['document_type'], 'pdf_document')
        self.assertEqual(metadata['page_count'], 10)
        self.assertEqual(metadata['pdf_version'], '1.7')
        self.assertEqual(metadata['page_width'], 8.5)
        self.assertEqual(metadata['page_height'], 11.0)
        self.assertTrue(metadata['pdfa_compliant'])
        
        # Test JSON document validation with schema
        json_data = [{
            'content': '{"key": "value"}',
            'metadata': {
                'source': 'test.json',
                'timestamp': '2024-01-01',
                'schema_version': '1.0',
                'root_element_count': 1,
                'schema_definition': {
                    'type': 'object',
                    'properties': {
                        'key': {'type': 'string'}
                    }
                }
            }
        }]
        
        formatted = self.formatter.format(json_data)
        metadata = formatted[0]['metadata']
        self.assertEqual(metadata['document_type'], 'json_document')
        self.assertEqual(metadata['schema_version'], '1.0')
        self.assertEqual(metadata['root_element_count'], 1)
        self.assertIn('schema_definition', metadata)

    def test_html_document_validation(self):
        """Test HTML document validation rules."""
        html_data = [{
            'content': '<!DOCTYPE html><html><body>Test</body></html>',
            'metadata': {
                'source': 'test.html',
                'timestamp': '2024-01-01',
                'html_version': 'html5',
                'has_doctype': True,
                'doctype': 'html5',
                'css_count': 0,
                'js_count': 0
            }
        }]
        
        formatted = self.formatter.format(html_data)
        metadata = formatted[0]['metadata']
        self.assertEqual(metadata['document_type'], 'html_document')
        self.assertEqual(metadata['html_version'], 'html5')
        self.assertTrue(metadata['has_doctype'])
        
    def test_csv_document_validation(self):
        """Test CSV document validation rules."""
        csv_data = [{
            'content': 'name,age,city\nJohn,30,New York',
            'metadata': {
                'source': 'test.csv',
                'timestamp': '2024-01-01',
                'column_count': 3,
                'header_row': True,
                'delimiter': ',',
                'row_count': 1,
                'has_quotes': False
            }
        }]
        
        formatted = self.formatter.format(csv_data)
        metadata = formatted[0]['metadata']
        self.assertEqual(metadata['document_type'], 'csv_document')
        self.assertEqual(metadata['column_count'], 3)
        self.assertTrue(metadata['header_row'])
        self.assertEqual(metadata['delimiter'], ',')

    def test_empty_data_handling(self):
        """Test formatting of empty data."""
        formatted = self.formatter.format([])
        self.assertEqual(len(formatted), 0)

if __name__ == '__main__':
    unittest.main()
