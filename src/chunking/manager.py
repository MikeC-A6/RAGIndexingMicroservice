from typing import Dict, Type, List, Any, Optional
from .base import BaseChunker
from .sentence_chunker import SentenceChunker

class ChunkerManager:
    """Manages document chunking strategies and their execution."""

    def __init__(self):
        """Initialize the chunker manager with default strategies."""
        self._strategies: Dict[str, Type[BaseChunker]] = {}
        # Register default chunking strategies
        self._register_default_strategies()

    def _register_default_strategies(self) -> None:
        """Register all default chunking strategies."""
        self.register_strategy(SentenceChunker)

    def register_strategy(self, strategy_class: Type[BaseChunker]) -> None:
        """
        Register a new chunking strategy.

        Args:
            strategy_class: The chunking strategy class to register
        """
        # Create an instance to get the strategy name
        strategy = strategy_class()
        # Store the class, not the instance
        self._strategies[strategy.strategy_name] = strategy_class

    def get_strategy(self, strategy_name: str) -> BaseChunker:
        """
        Get a chunking strategy by name.

        Args:
            strategy_name: Name of the strategy to retrieve

        Returns:
            An instance of the requested chunking strategy

        Raises:
            ValueError: If strategy_name is not registered
        """
        if strategy_name not in self._strategies:
            available = list(self._strategies.keys())
            raise ValueError(f"Unknown strategy: {strategy_name}. Available strategies: {available}")
        return self._strategies[strategy_name]()

    def get_available_strategies(self) -> List[str]:
        """Return list of available chunking strategies."""
        return list(self._strategies.keys())

    def apply_chunking(self, 
                      strategy_name: str, 
                      content: str, 
                      metadata: Dict[str, Any],
                      chunk_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Apply a chunking strategy to document content.

        Args:
            strategy_name: Name of the chunking strategy to use
            content: Document content to chunk
            metadata: Document metadata
            chunk_params: Optional parameters for the chunking strategy

        Returns:
            List of chunks with their metadata

        Raises:
            ValueError: If strategy_name is not registered
        """
        strategy = self.get_strategy(strategy_name)
        return strategy.chunk_document(content, metadata, chunk_params)