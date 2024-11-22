from typing import List, Dict, Any

class OutputFormatter:
    """Formats indexed data for the Embedding Service."""
    
    def format(self, indexed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format indexed data into standardized output."""
        formatted_output = []

        for item in indexed_data:
            # Keep all metadata fields by copying the entire metadata dict
            formatted_chunk = {
                'text': item.get('content', ''),
                'metadata': item.get('metadata', {})
            }
            formatted_output.append(formatted_chunk)

        return formatted_output
