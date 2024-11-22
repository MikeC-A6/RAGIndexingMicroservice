from typing import Dict, Type, List, Any
from src.indexing.base import BaseIndexer
from src.indexing.strategies.simple_directory_reader import SimpleDirectoryReader
from src.indexing.strategies.json_indexer import JSONIndexer

class StrategyManager:
    """Manages indexing strategies and their execution."""
    
    def __init__(self):
        self._strategies: Dict[str, Type[BaseIndexer]] = {
            'simple_directory': SimpleDirectoryReader,
            'json_index': JSONIndexer
        }
    
    def apply_strategy(self, strategy_name: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply the specified indexing strategy to the documents."""
        if strategy_name not in self._strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy = self._strategies[strategy_name]()
        return strategy.index(documents)
    
    def get_available_strategies(self) -> List[str]:
        """Return list of available indexing strategies."""
        return list(self._strategies.keys())
