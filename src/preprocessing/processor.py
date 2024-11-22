from typing import List, Dict, Any
from src.preprocessing.extractors.text_extractor import TextExtractor
from src.preprocessing.extractors.pdf_extractor import PDFExtractor

class PreprocessingModule:
    """Handles document preprocessing operations."""
    
    def __init__(self):
        self.extractors = {
            'txt': TextExtractor(),
            'pdf': PDFExtractor()
        }
    
    def process(self, documents: List[Dict[str, Any]], options: Dict = None) -> List[Dict[str, Any]]:
        """Process documents according to their type and specified options."""
        processed_docs = []
        options = options or {}
        
        for doc in documents:
            # Extract document type and content
            doc_type = doc.get('type', 'txt')
            content = doc.get('content', '')
            
            # Get appropriate extractor
            extractor = self.extractors.get(doc_type)
            if not extractor:
                raise ValueError(f"Unsupported document type: {doc_type}")
            
            # Extract and clean text
            processed_content = extractor.extract(content)
            
            # Chunk if necessary
            if options.get('chunk_size'):
                processed_content = self._chunk_text(
                    processed_content,
                    options['chunk_size']
                )
            
            processed_docs.append({
                'content': processed_content,
                'metadata': doc.get('metadata', {})
            })
        
        return processed_docs
    
    def _chunk_text(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks of specified size."""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
