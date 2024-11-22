import base64
from typing import Optional
import PyPDF2
from io import BytesIO

class PDFExtractor:
    """Handles extraction of text from PDF documents."""

    def extract(self, content: Optional[str] = None, file_path: Optional[str] = None) -> str:
        """
        Extract text from PDF content or file.

        Args:
            content: Base64 encoded PDF content or raw PDF text
            file_path: Path to PDF file (used if content is None)

        Returns:
            Extracted text content
        """
        try:
            if file_path:
                return self._extract_from_file(file_path)
            elif content:
                pdf_content = self._decode_pdf_content(content)
                return self._extract_text_from_pdf(pdf_content)
            else:
                raise ValueError("Either content or file_path must be provided")

        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def _decode_pdf_content(self, content: str) -> bytes:
        """
        Decode base64 PDF content.

        Args:
            content: Base64 encoded PDF content

        Returns:
            Decoded PDF bytes
        """
        try:
            return base64.b64decode(content)
        except Exception:
            raise ValueError("Invalid PDF content encoding")

    def _extract_from_file(self, file_path: str) -> str:
        """
        Extract text directly from a PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            with open(file_path, 'rb') as file:
                return self._extract_text_from_pdf(file.read())
        except Exception as e:
            raise ValueError(f"Failed to read PDF file: {str(e)}")

    def _extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF bytes.

        Args:
            pdf_content: PDF content as bytes

        Returns:
            Extracted text
        """
        try:
            pdf_file = BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = []
            for page in pdf_reader.pages:
                text.append(page.extract_text())

            return "\n".join(text)

        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF content: {str(e)}")