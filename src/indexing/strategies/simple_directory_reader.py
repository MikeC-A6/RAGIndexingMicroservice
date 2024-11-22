from typing import List, Dict, Any, Optional
from src.indexing.base import BaseIndexer
from llama_index.core.readers import SimpleDirectoryReader as LlamaDirectoryReader
import os
from datetime import datetime

class SimpleDirectoryReader(BaseIndexer):
    """Implements directory-based document indexing strategy using LlamaIndex."""
    
    def __init__(self):
        """Initialize the SimpleDirectoryReader strategy."""
        super().__init__()
    
    @property
    def strategy_name(self) -> str:
        return "simple_directory"
    
    def index(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process documents from a directory using LlamaIndex's SimpleDirectoryReader.
        
        Args:
            documents: List of documents with directory paths in metadata
            
        Returns:
            List of indexed document chunks with metadata
        """
        indexed_documents = []
        
        for doc in documents:
            metadata = doc.get('metadata', {})
            directory_path = metadata.get('directory_path')
            
            if not directory_path or not os.path.isdir(directory_path):
                continue
                
            # Use LlamaIndex's SimpleDirectoryReader to process the directory
            reader = LlamaDirectoryReader(
                input_dir=directory_path,
                recursive=True,
                filename_as_id=True
            )
            
            # Load and process documents
            llama_docs = reader.load_data()
            
            # Convert LlamaIndex documents to our format
            for idx, llama_doc in enumerate(llama_docs):
                doc_metadata = {
                    'source': llama_doc.metadata.get('file_path', ''),
                    'chunk_index': idx,
                    'timestamp': datetime.now().isoformat(),
                    'strategy': self.strategy_name,
                    'file_type': os.path.splitext(llama_doc.metadata.get('file_path', ''))[1],
                    'original_metadata': llama_doc.metadata
                }
                
                indexed_chunk = {
                    'content': llama_doc.text,
                    'metadata': doc_metadata
                }
                
                indexed_documents.append(indexed_chunk)
        
        return indexed_documents
