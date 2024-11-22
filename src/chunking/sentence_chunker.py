from typing import List, Dict, Any, Optional
import nltk
from nltk.tokenize import sent_tokenize
from .base import BaseChunker

class SentenceChunker(BaseChunker):
    """Implements sentence-based document chunking with configurable parameters."""

    def __init__(self):
        """Initialize the sentence chunker and download required NLTK data."""
        try:
            # Download both required NLTK resources
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        except Exception as e:
            raise RuntimeError(f"Failed to download NLTK resources: {str(e)}")

    @property
    def strategy_name(self) -> str:
        return "sentence_chunker"

    def validate_params(self, chunk_params: Dict[str, Any]) -> None:
        """
        Validate chunking parameters.

        Args:
            chunk_params: Dictionary containing:
                - min_sentence_length: Minimum length of a sentence to be considered
                - max_sentences_per_chunk: Maximum number of sentences per chunk
                - overlap_sentences: Number of sentences to overlap between chunks
                - language: Language code for sentence detection (default: 'english')

        Raises:
            ValueError: If parameters are invalid
        """
        if chunk_params:
            min_length = chunk_params.get('min_sentence_length', 0)
            max_sentences = chunk_params.get('max_sentences_per_chunk', 0)
            overlap = chunk_params.get('overlap_sentences', 0)

            if min_length < 0:
                raise ValueError("min_sentence_length must be non-negative")
            if max_sentences <= 0:
                raise ValueError("max_sentences_per_chunk must be positive")
            if overlap < 0:
                raise ValueError("overlap_sentences must be non-negative")
            if overlap >= max_sentences:
                raise ValueError("overlap_sentences must be less than max_sentences_per_chunk")

    def chunk_document(self, content: str, metadata: Dict[str, Any],
                      chunk_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Chunk the document into sentence-based chunks according to parameters.

        Args:
            content: Document content to chunk
            metadata: Document metadata
            chunk_params: Optional parameters controlling chunking behavior

        Returns:
            List of chunks with their metadata
        """
        # Set default parameters if not provided
        params = {
            'min_sentence_length': 10,
            'max_sentences_per_chunk': 5,
            'overlap_sentences': 1,
            'language': 'english'
        }
        if chunk_params:
            params.update(chunk_params)

        # Validate parameters
        self.validate_params(params)

        # Tokenize content into sentences using punkt tokenizer
        try:
            sentences = nltk.sent_tokenize(content)
        except Exception as e:
            raise RuntimeError(f"Failed to perform sentence tokenization: {str(e)}")

        # Filter out short sentences
        sentences = [s for s in sentences if len(s) >= params['min_sentence_length']]

        if not sentences:
            return [{
                'content': content,
                'metadata': {**metadata, 'strategy': self.strategy_name}
            }]

        chunks = []
        max_sentences = params['max_sentences_per_chunk']
        overlap = params['overlap_sentences']
        
        # Create chunks with overlap
        for i in range(0, len(sentences), max_sentences - overlap):
            chunk_sentences = sentences[i:i + max_sentences]
            if chunk_sentences:
                chunk_content = ' '.join(chunk_sentences)
                chunk_metadata = {
                    **metadata,
                    'strategy': self.strategy_name,
                    'chunk_index': len(chunks),
                    'sentences_count': len(chunk_sentences),
                    'start_sentence_index': i
                }
                chunks.append({
                    'content': chunk_content,
                    'metadata': chunk_metadata
                })

        return chunks
