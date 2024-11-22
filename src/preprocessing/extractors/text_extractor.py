class TextExtractor:
    """Handles extraction and cleaning of plain text documents."""
    
    def extract(self, content: str) -> str:
        """
        Extract and clean text content.
        
        Args:
            content: Raw text content
            
        Returns:
            Cleaned text content
        """
        # Remove extra whitespace
        cleaned_text = ' '.join(content.split())
        
        # Basic text cleaning
        cleaned_text = self._clean_text(cleaned_text)
        
        return cleaned_text
    
    def _clean_text(self, text: str) -> str:
        """
        Apply basic text cleaning operations.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove special characters but keep basic punctuation
        cleaned = ''.join(char for char in text if char.isprintable())
        
        # Normalize whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
