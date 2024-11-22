from typing import Dict, Type, List, Any, Optional
from .base import BaseChunker

class ChunkerManager:
    """Manages document chunking strategies and their execution."""
    
    def __init__(self):
        """Initialize the chunker manager with an empty strategy registry."""
        self._strategies: Dict[str, Type[BaseChunker]] = {}
        
    def register_strategy(self, strategy_class: Type[BaseChunker]) -> None:
        """
        Register a new chunking strategy.
        
        Args:
            strategy_class: The chunking strategy class to register
        """
        strategy = strategy_class()
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
            raise ValueError(f"Unknown chunking strategy: {strategy_name}")
        return self._strategies[strategy_name]()
        
    def apply_chunking(self, strategy_name: str, content: str, 
                      metadata: Dict[str, Any],
                      chunk_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Apply a chunking strategy to document content.
        
        Args:
            strategy_name: Name of the strategy to apply
            content: Document content to chunk
            metadata: Document metadata
            chunk_params: Optional parameters for chunking
            
        Returns:
            List of chunks with their metadata
        """
        strategy = self.get_strategy(strategy_name)
        
        # Validate parameters if provided
        if chunk_params:
            strategy.validate_params(chunk_params)
            
        return strategy.chunk_document(content, metadata, chunk_params)
        
    def get_available_strategies(self) -> List[str]:
        """Return list of available chunking strategies."""
        return list(self._strategies.keys())
