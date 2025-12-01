import re
from pathlib import Path
from typing import List, Optional

def hydrate_markdown_content(text: str, search_roots: Optional[List[str]] = None) -> str:
    """
    Scans the markdown text for specific citation patterns and injects 
    the actual file content.
    
    Target Pattern: *(Table source: path/to/file.md)*
    Action: Replaces that line with the content of file.md
    """
    
    # Default to empty list if no roots provided
    if search_roots is None:
        search_roots = []

    # Regex Breakdown:
    # \*?             -> Optional italics syntax (start)
    # \(Table source: -> Literal text
    # \s* -> Optional whitespace
    # (.*?)           -> CAPTURE GROUP 1: The file path
    # \)              -> Closing parenthesis
    # \*?             -> Optional italics syntax (end)
    pattern = r'\*?\(Table source:\s*(.*?)\)\*?'

    def replace_match(match):
        # Extract the path from the capture group
        raw_path = match.group(1).strip()
        
        # Clean path (remove any stray whitespace or quotes)
        clean_path = raw_path.strip("'\"")
        
        p = Path(clean_path)
        
        # Security: Prevent traversing up directories
        if ".." in str(p):
            return f"\n*[Security: Relative paths with '..' are not allowed: {clean_path}]*\n"

        # Search for the file:
        # 1. Check the path exactly as written (relative to current CWD)
        # 2. Check relative to any provided search_roots
        candidates = [p]
        for root in search_roots:
            candidates.append(Path(root) / p)
        
        target_file = None
        for cand in candidates:
            if cand.exists() and cand.is_file():
                target_file = cand
                break
        
        if target_file:
            try:
                # Read the content
                content = target_file.read_text(encoding='utf-8')
                
                # Check if the content is CSV (fallback logic)
                if target_file.suffix.lower() == '.csv':
                    return f"\n\n**Data ({target_file.name}):**\n```csv\n{content}\n```\n\n"
                
                # Default: Return raw markdown content (Embedded)
                return f"\n\n{content}\n\n"
            
            except Exception as e:
                return f"\n*[Error reading file {clean_path}: {str(e)}]*\n"
        else:
            return f"\n*[Referenced file not found: {clean_path}]*\n"

    # Perform the substitution using Regex
    hydrated_text = re.sub(pattern, replace_match, text)
    
    return hydrated_text