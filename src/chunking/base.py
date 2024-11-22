from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseChunker(ABC):
    """Base interface for document chunking strategies."""

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Return the name of the chunking strategy."""
        pass

    @abstractmethod
    def chunk_document(self, content: str, metadata: Dict[str, Any], 
                      chunk_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Chunk the document content according to the strategy and parameters.

        Args:
            content: The document content to chunk
            metadata: Document metadata
            chunk_params: Optional parameters to control chunking behavior

        Returns:
            List of chunks, each containing the chunk content and associated metadata
        """
        pass

    @abstractmethod
    def validate_params(self, chunk_params: Dict[str, Any]) -> None:
        """
        Validate chunking parameters for this strategy.

        Args:
            chunk_params: Parameters to validate

        Raises:
            ValueError: If parameters are invalid
        """
        pass
