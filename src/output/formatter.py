from typing import List, Dict, Any

class OutputFormatter:
    """Formats indexed data for the Embedding Service."""
    
    def format(self, indexed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format indexed data into standardized output."""
        formatted_output = []
        
        for item in indexed_data:
            formatted_chunk = {
                'text': item.get('content', ''),
                'metadata': {
                    'source': item.get('metadata', {}).get('source'),
                    'chunk_index': item.get('metadata', {}).get('chunk_index'),
                    'timestamp': item.get('metadata', {}).get('timestamp')
                }
            }
            formatted_output.append(formatted_chunk)
        
        return formatted_output
