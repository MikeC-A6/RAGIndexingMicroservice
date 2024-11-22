import unittest
from typing import Dict, Any, List, Optional
from src.chunking.base import BaseChunker
from src.chunking.manager import ChunkerManager

class SimpleTestChunker(BaseChunker):
    """A simple chunker implementation for testing."""
    
    @property
    def strategy_name(self) -> str:
        return "simple_test_chunker"
        
    def validate_params(self, chunk_params: Dict[str, Any]) -> None:
        if chunk_params.get('chunk_size', 0) <= 0:
            raise ValueError("chunk_size must be positive")
            
    def chunk_document(self, content: str, metadata: Dict[str, Any],
                      chunk_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        chunk_size = chunk_params.get('chunk_size', 100) if chunk_params else 100
        chunks = [content[i:i + chunk_size] 
                 for i in range(0, len(content), chunk_size)]
        
        return [
            {
                'content': chunk,
                'metadata': {
                    **metadata,
                    'chunk_index': idx,
                    'chunk_size': len(chunk),
                    'strategy': self.strategy_name
                }
            }
            for idx, chunk in enumerate(chunks)
        ]

class TestChunking(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ChunkerManager()
        self.manager.register_strategy(SimpleTestChunker)
        
    def test_strategy_registration(self):
        """Test chunking strategy registration."""
        strategies = self.manager.get_available_strategies()
        self.assertIn('simple_test_chunker', strategies)
        
    def test_strategy_retrieval(self):
        """Test chunking strategy retrieval."""
        strategy = self.manager.get_strategy('simple_test_chunker')
        self.assertIsInstance(strategy, SimpleTestChunker)
        
        with self.assertRaises(ValueError):
            self.manager.get_strategy('non_existent_strategy')
            
    def test_chunking_with_params(self):
        """Test document chunking with parameters."""
        content = "This is a test document that needs to be chunked into smaller pieces."
        metadata = {'source': 'test.txt', 'type': 'text'}
        chunk_params = {'chunk_size': 10}
        
        chunks = self.manager.apply_chunking(
            'simple_test_chunker',
            content,
            metadata,
            chunk_params
        )
        
        self.assertTrue(len(chunks) > 0)
        self.assertEqual(len(chunks[0]['content']), 10)
        self.assertEqual(chunks[0]['metadata']['strategy'], 'simple_test_chunker')
        self.assertEqual(chunks[0]['metadata']['chunk_index'], 0)
        
    def test_invalid_chunk_params(self):
        """Test validation of invalid chunking parameters."""
        content = "Test content"
        metadata = {'source': 'test.txt'}
        invalid_params = {'chunk_size': -1}
        
        with self.assertRaises(ValueError):
            self.manager.apply_chunking(
                'simple_test_chunker',
                content,
                metadata,
                invalid_params
            )
            
    def test_chunking_without_params(self):
        """Test chunking with default parameters."""
        content = "Short test content"
        metadata = {'source': 'test.txt'}
        
        chunks = self.manager.apply_chunking(
            'simple_test_chunker',
            content,
            metadata
        )
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]['content'], content)
        self.assertEqual(chunks[0]['metadata']['strategy'], 'simple_test_chunker')

if __name__ == '__main__':
    unittest.main()
