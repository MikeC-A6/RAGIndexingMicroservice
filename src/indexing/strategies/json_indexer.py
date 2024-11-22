from typing import List, Dict, Any
import json
from src.indexing.base import BaseIndexer

class JSONIndexer(BaseIndexer):
    """Implements JSON document indexing strategy."""
    
    @property
    def strategy_name(self) -> str:
        return "json_index"
    
    def index(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process JSON documents and create indexed chunks.
        
        Args:
            documents: List of preprocessed JSON documents with content and metadata
            
        Returns:
            List of indexed document chunks with metadata
        """
        indexed_documents = []
        
        for doc in documents:
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            try:
                # Parse JSON content if string
                if isinstance(content, str):
                    content = json.loads(content)
                
                # Flatten JSON structure for indexing
                flattened_content = self._flatten_json(content)
                
                # Create indexed chunks
                for key, value in flattened_content.items():
                    indexed_chunk = {
                        'content': str(value),
                        'metadata': {
                            'source': metadata.get('source', ''),
                            'json_path': key,
                            'timestamp': metadata.get('timestamp'),
                            'strategy': self.strategy_name
                        }
                    }
                    indexed_documents.append(indexed_chunk)
                    
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON content: {str(e)}")
                
        return indexed_documents
    
    def _flatten_json(self, json_obj: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten nested JSON structure into dot-notation keys."""
        items = []
        for k, v in json_obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
