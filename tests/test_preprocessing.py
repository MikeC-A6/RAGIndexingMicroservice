import unittest
import os
from src.preprocessing.processor import PreprocessingModule
from src.preprocessing.extractors import TextExtractor, PDFExtractor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = PreprocessingModule()
        self.text_extractor = TextExtractor()
        self.pdf_extractor = PDFExtractor()
        self.test_docs_dir = "test_docs"

    def test_text_extraction(self):
        """Test text extraction and cleaning."""
        test_content = "  Test   content  with   extra   spaces  "
        cleaned = self.text_extractor.extract(test_content)
        self.assertEqual(cleaned, "Test content with extra spaces")

    def test_pdf_extraction(self):
        """Test PDF text extraction."""
        test_pdf_path = os.path.join(self.test_docs_dir, "Test_PDF1.pdf")

        if not os.path.exists(test_pdf_path):
            self.skipTest(f"Test PDF not found at {test_pdf_path}")

        # Test extraction from file
        extracted = self.pdf_extractor.extract(file_path=test_pdf_path)
        self.assertTrue(isinstance(extracted, str))
        self.assertTrue(len(extracted) > 0)
        print(f"\nExtracted PDF content length: {len(extracted)}")
        print(f"First 200 characters: {extracted[:200]}")

    def test_document_processing(self):
        """Test complete document processing."""
        test_pdf_path = os.path.join(self.test_docs_dir, "Test_PDF1.pdf")

        if not os.path.exists(test_pdf_path):
            self.skipTest(f"Test PDF not found at {test_pdf_path}")

        test_docs = [{
            'content': '',
            'type': 'pdf',
            'metadata': {
                'source': test_pdf_path,
                'file_path': test_pdf_path
            }
        }]

        processed = self.preprocessor.process(test_docs)
        self.assertTrue(len(processed) > 0)
        self.assertTrue('content' in processed[0])
        self.assertTrue('metadata' in processed[0])
        self.assertTrue(len(processed[0]['content']) > 0)

if __name__ == '__main__':
    unittest.main()
