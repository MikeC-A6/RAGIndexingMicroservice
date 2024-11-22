from typing import List, Dict, Any
from src.indexing.base import BaseIndexer
import os

class SimpleDirectoryReader(BaseIndexer):
    """Implements directory-based document indexing strategy."""
    
    @property
    def strategy_name(self) -> str:
        return "simple_directory"
    
    def index(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process documents from a directory and create indexed chunks.
        
        Args:
            documents: List of preprocessed documents with content and metadata
            
        Returns:
            List of indexed document chunks with metadata
        """
        indexed_documents = []
        
        for doc in documents:
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            # Create indexed chunks with metadata
            indexed_chunk = {
                'content': content,
                'metadata': {
                    'source': metadata.get('source', ''),
                    'chunk_index': metadata.get('chunk_index', 0),
                    'timestamp': metadata.get('timestamp'),
                    'strategy': self.strategy_name
                }
            }
            
            indexed_documents.append(indexed_chunk)
            
        return indexed_documents
