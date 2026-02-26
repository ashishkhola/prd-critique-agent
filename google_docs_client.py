"""
Google Docs Client for reading document content

Requires Google Cloud service account credentials or OAuth2 setup
"""

import json
from typing import Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocsClient:
    """Client for reading Google Docs documents"""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Docs client

        Args:
            credentials_path: Path to service account JSON credentials file
                            If None, will use application default credentials
        """
        if credentials_path:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/documents.readonly']
            )
        else:
            # Use application default credentials
            from google.auth import default
            self.credentials, _ = default(
                scopes=['https://www.googleapis.com/auth/documents.readonly']
            )

        self.service = build('docs', 'v1', credentials=self.credentials)

    def read_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Read content from a Google Doc

        Args:
            doc_id: The Google Doc ID

        Returns:
            Dictionary with document content and metadata
        """
        try:
            # Fetch document
            document = self.service.documents().get(documentId=doc_id).execute()

            # Extract content
            title = document.get('title', 'Untitled')
            body_content = document.get('body', {}).get('content', [])

            # Parse content into readable text
            text_content = self._parse_structural_elements(body_content)

            return {
                "success": True,
                "doc_id": doc_id,
                "title": title,
                "content": text_content,
                "raw_document": document
            }

        except HttpError as e:
            return {
                "success": False,
                "error": str(e),
                "doc_id": doc_id
            }

    def _parse_structural_elements(self, elements: list) -> str:
        """Parse Google Docs structural elements into plain text"""
        text_parts = []

        for element in elements:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                paragraph_text = self._parse_paragraph(paragraph)
                if paragraph_text:
                    text_parts.append(paragraph_text)

            elif 'table' in element:
                # Handle tables
                table = element['table']
                table_text = self._parse_table(table)
                if table_text:
                    text_parts.append(table_text)

            elif 'sectionBreak' in element:
                text_parts.append("\n---\n")

        return "\n\n".join(text_parts)

    def _parse_paragraph(self, paragraph: dict) -> str:
        """Parse a paragraph element"""
        elements = paragraph.get('elements', [])
        paragraph_text = []

        for elem in elements:
            if 'textRun' in elem:
                text_run = elem['textRun']
                content = text_run.get('content', '')

                # Check for styling
                text_style = text_run.get('textStyle', {})

                # Apply markdown formatting based on style
                if text_style.get('bold'):
                    content = f"**{content.strip()}**"
                if text_style.get('italic'):
                    content = f"*{content.strip()}*"

                paragraph_text.append(content)

        # Check paragraph style for headings
        paragraph_style = paragraph.get('paragraphStyle', {})
        named_style_type = paragraph_style.get('namedStyleType', '')

        full_text = ''.join(paragraph_text).strip()

        if not full_text:
            return ""

        # Apply heading formatting
        if 'HEADING_1' in named_style_type:
            return f"# {full_text}"
        elif 'HEADING_2' in named_style_type:
            return f"## {full_text}"
        elif 'HEADING_3' in named_style_type:
            return f"### {full_text}"
        elif 'HEADING_4' in named_style_type:
            return f"#### {full_text}"
        elif 'HEADING_5' in named_style_type:
            return f"##### {full_text}"
        elif 'HEADING_6' in named_style_type:
            return f"###### {full_text}"

        return full_text

    def _parse_table(self, table: dict) -> str:
        """Parse a table element into markdown table"""
        table_rows = table.get('tableRows', [])
        markdown_rows = []

        for i, row in enumerate(table_rows):
            cells = row.get('tableCells', [])
            cell_contents = []

            for cell in cells:
                content = cell.get('content', [])
                cell_text = self._parse_structural_elements(content)
                cell_contents.append(cell_text.strip())

            markdown_rows.append("| " + " | ".join(cell_contents) + " |")

            # Add header separator after first row
            if i == 0:
                separator = "| " + " | ".join(["---"] * len(cell_contents)) + " |"
                markdown_rows.append(separator)

        return "\n".join(markdown_rows)

    @staticmethod
    def extract_doc_id(url: str) -> Optional[str]:
        """
        Extract document ID from a Google Docs URL

        Args:
            url: Google Docs URL

        Returns:
            Document ID or None if not found
        """
        import re

        # Pattern: https://docs.google.com/document/d/{DOC_ID}/...
        pattern = r'/document/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)

        if match:
            return match.group(1)

        # If no pattern match, assume the input is already a doc ID
        return url if len(url) > 20 else None


# Standalone function for integration with agent
def read_google_doc(doc_id: str, credentials_path: Optional[str] = None) -> str:
    """
    Read Google Doc and return JSON string result

    Args:
        doc_id: Document ID or URL
        credentials_path: Path to service account credentials

    Returns:
        JSON string with document content
    """
    try:
        # Extract doc ID from URL if necessary
        actual_doc_id = GoogleDocsClient.extract_doc_id(doc_id)
        if not actual_doc_id:
            return json.dumps({
                "success": False,
                "error": "Invalid document ID or URL"
            })

        # Read document
        client = GoogleDocsClient(credentials_path)
        result = client.read_document(actual_doc_id)

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to read document: {str(e)}"
        })
