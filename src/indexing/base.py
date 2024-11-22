from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseIndexer(ABC):
    """Base class for all indexing strategies."""
    
    @abstractmethod
    def index(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process documents and return indexed data."""
        pass
    
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Return the name of the strategy."""
        pass
