import unittest
from src.chunking.sentence_chunker import SentenceChunker

class TestSentenceChunker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.chunker = SentenceChunker()
        self.test_content = (
            "This is the first sentence. This is the second sentence. "
            "Here comes the third one! And this is sentence four. "
            "Finally, this is the fifth sentence. And a sixth one here. "
            "Seven is lucky. Eight is great. Nine is fine. Ten is the end."
        )
        self.metadata = {'source': 'test.txt', 'type': 'text'}

    def test_default_chunking(self):
        """Test chunking with default parameters."""
        chunks = self.chunker.chunk_document(
            self.test_content,
            self.metadata
        )
        self.assertTrue(len(chunks) > 0)
        self.assertEqual(chunks[0]['metadata']['strategy'], 'sentence_chunker')

    def test_custom_chunk_size(self):
        """Test chunking with custom max sentences per chunk."""
        params = {
            'max_sentences_per_chunk': 3,
            'overlap_sentences': 1
        }
        chunks = self.chunker.chunk_document(
            self.test_content,
            self.metadata,
            params
        )
        self.assertTrue(all(
            chunk['metadata']['sentences_count'] <= 3 
            for chunk in chunks
        ))

    def test_invalid_params(self):
        """Test validation of invalid parameters."""
        invalid_params = {
            'max_sentences_per_chunk': 0,
            'overlap_sentences': 1
        }
        with self.assertRaises(ValueError):
            self.chunker.validate_params(invalid_params)

        invalid_params = {
            'max_sentences_per_chunk': 3,
            'overlap_sentences': 3
        }
        with self.assertRaises(ValueError):
            self.chunker.validate_params(invalid_params)

    def test_min_sentence_length(self):
        """Test minimum sentence length filtering."""
        params = {
            'min_sentence_length': 20,
            'max_sentences_per_chunk': 5
        }
        chunks = self.chunker.chunk_document(
            self.test_content,
            self.metadata,
            params
        )
        # Verify that short sentences are filtered out
        for chunk in chunks:
            sentences = chunk['content'].split('.')
            self.assertTrue(all(
                len(s.strip()) >= 20 
                for s in sentences 
                if s.strip()
            ))

if __name__ == '__main__':
    unittest.main()
