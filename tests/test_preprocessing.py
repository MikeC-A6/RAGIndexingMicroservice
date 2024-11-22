import unittest
from src.preprocessing.processor import PreprocessingModule
from src.preprocessing.extractors import TextExtractor, PDFExtractor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = PreprocessingModule()
        self.text_extractor = TextExtractor()
        self.pdf_extractor = PDFExtractor()
        
    def test_text_extraction(self):
        """Test text extraction and cleaning."""
        test_content = "  Test   content  with   extra   spaces  "
        cleaned = self.text_extractor.extract(test_content)
        self.assertEqual(cleaned, "Test content with extra spaces")
        
    def test_pdf_extraction(self):
        """Test PDF text extraction."""
        # Create mock PDF content
        test_content = "mock_pdf_content"
        extracted = self.pdf_extractor.extract(test_content)
        self.assertTrue(isinstance(extracted, str))
        
    def test_document_processing(self):
        """Test complete document processing."""
        test_docs = [{
            'content': 'Test content',
            'type': 'txt',
            'metadata': {'source': 'test.txt'}
        }]
        
        processed = self.preprocessor.process(test_docs)
        self.assertTrue(len(processed) > 0)
        self.assertTrue('content' in processed[0])
        self.assertTrue('metadata' in processed[0])

if __name__ == '__main__':
    unittest.main()
