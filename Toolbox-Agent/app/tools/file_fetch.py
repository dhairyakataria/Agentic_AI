from pathlib import Path
import time
from langchain.tools import tool

ALLOWED_DIR = Path(__file__).resolve().parents[1] / "data" / "allowed_files"

@tool
def file_fetch(filename: str) -> str:
    """
    Read contents of a file from the data/allowed_files directory.
    
    Use this tool to:
    - Read text files
    - Access stored documents
    - Retrieve file contents
    
    Args:
        filename: Name of the file in data/allowed_files (e.g., "sample.txt")
    
    Returns:
        File contents as string
    
    Security:
        - Only files in data/allowed_files directory are accessible
        - Path traversal attempts are blocked
    """
    try:
        # Security: Resolve path and prevent traversal attacks
        file_path = (ALLOWED_DIR / filename).resolve()
        print("==========================")
        print(file_path)
        # Ensure file is within allowed directory
        if not str(file_path).startswith(str(ALLOWED_DIR.resolve())):
            return "Error: Access denied - attempted path traversal detected."
        
        # Check file exists
        if not file_path.exists():
            available_files = [f.name for f in file_path.glob("*") if f.is_file()]
            return f"Error: File '{filename}' not found.\nAvailable files: {', '.join(available_files) if available_files else 'None'}"
        
        # Read and return contents
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"File: {filename}\n{'='*50}\n{content}"
    
    except Exception as e:
        return f"File read error: {str(e)}"
