import re


def _clean_branch_name(raw: str) -> str:
    """Strip trailing 'Branch' / 'Church' suffix the user or entity extractor may include."""
    return re.sub(r'\s+(branch|church)$', '', raw.strip(), flags=re.IGNORECASE).strip()
